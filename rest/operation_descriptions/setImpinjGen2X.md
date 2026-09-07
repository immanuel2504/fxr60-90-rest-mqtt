## 1. Description

The `PUT /cloud/impinjGen2X` REST endpoint configures Impinj Gen2X proprietary RFID features on the reader.

This endpoint allows you to configure:

- FastID tag TID embedding through `fastID`
- Tag protection and visibility control through `tagProtect`
- TagFocus session suppression through `tagFocus`
- Tag quieting (basic or advanced) through `tagQuieting`

Use this endpoint to:

- Enable FastID to embed the TID in every inventory response without a separate read
- Protect specific tags with a 32-bit password to prevent unauthorized reads
- Enable TagFocus to improve read rates in dense tag environments by suppressing already-inventoried tags
- Quiet specific tags (by EPC) to exclude them from inventory responses

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_impinjGen2X` |
| Pattern Name | Impinj Gen2X Configuration |
| REST Endpoint | `PUT /cloud/impinjGen2X` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Success Response | `200 OK` |
| Error Responses | `422 Unprocessable Entity`, `500 Internal Server Error` |
| Supported Features | `fastID`, `tagProtect`, `tagFocus`, `tagQuieting` |
| Supported TagProtect Actions | `enableTagProtection`, `disableTagProtection`, `enableTagVisibility`, `disableTagVisibility` |
| Supported TagQuieting Modes | `basic` (quiet/unquiet by EPC list), `advanced` (pre-select with mask) |
| Supported TagQuieting Basic Actions | `quiet`, `unquiet` |
| Supported Gen2 Memory Banks | EPC, TID, USER, RESERVED |
| Supported Select Targets | S0, S1, S2, S3, SL |
| Supported Tag Quiet Masks | S0A, S0B, S2A, S2B, S3A, S3B, SL_ASSERT, SL_DEASSERT |
| Mutually Exclusive Features | `fastID`, `tagProtect`, `tagFocus`, `tagQuieting` (exactly one feature object per request) |

## 3. Before You Begin

Decide which Gen2X feature to configure before sending this request. Send **exactly one** of `fastID`, `tagProtect`, `tagFocus`, or `tagQuieting`. An empty body or any combination of two or more features is rejected. To apply the saved configuration during inventory, send `PUT /cloud/start` with `applyImpinjGen2X: true`. After `PUT /cloud/stop`, send the flag again on the next start — apply is per inventory session.

**Prerequisite:** The target tag must have a valid 32-bit Access Password configured before using Protected Mode operations. The password parameter used in the TagProtect APIs is the same Access Password stored on the tag. These APIs do not create or assign a new password.

Write that password first with `PUT /cloud/mode` WRITE to the RESERVED bank, words 2–3. Then send the same 8-character hex value in `tagProtect.password`.

| What You Need | Details |
|---|---|
| Feature selection | Exactly one of `fastID`, `tagProtect`, `tagFocus`, or `tagQuieting` per request. An empty body or two features together is rejected. `tagProtect` cannot be combined with the others. |
| FastID | Decide whether to enable or disable TID embedding. |
| TagProtect action | Choose one of: `enableTagProtection` (protect a specific tag), `disableTagProtection` (remove protection from a tag), `enableTagVisibility` (allow reading protected tags), `disableTagVisibility` (block reading protected tags). |
| TagProtect password | An 8-character hex string (32-bit) is required for all TagProtect actions. This is the Access Password already stored on the tag. These APIs do not create or assign a new password. |
| TagProtect tag EPC | `tagID` (hex EPC) is required for `enableTagProtection` and `disableTagProtection`. It must be omitted for `enableTagVisibility` and `disableTagVisibility`. |
| TagFocus | Whether to enable or disable the feature. TagFocus targets session S1. |
| TagQuieting | For basic: provide `action` (`quiet`/`unquiet`) and the `tagIDs` EPC array (maximum 31 tag IDs per request). For advanced: provide the `preSelect` array, `tagQuietMasks`, `target`, and `stateAwareAction`. |
| Inventory state | Configure Gen2X before starting inventory. Stop any active inventory first with `PUT /cloud/stop`. |
| Activation | PUT only saves the configuration. Start with `applyImpinjGen2X: true` to apply it. After stop, a plain start does not re-apply it — send the flag on every start that should use Gen2X. |

## 4. Choosing a Gen2X Feature

The Gen2X feature you select determines the reader's behavior during inventory. Choose based on your operational goal.

| Feature | Description | Scope |
|---|---|---|
| `fastID` | Returns the EPC and TID together in a single read, eliminating the need for a separate TID read. Best for applications that require chip-level identity (anti-counterfeit, authentication). | Reader-scoped |
| `tagProtect` | Password-protects individual tags or controls reader visibility of protected tags. Use for securing sensitive items or restricting access. | Tag-scoped |
| `tagFocus` | Silences already-read tags so the reader focuses only on new tags entering the field. Ideal for portal and conveyor applications. | Reader-scoped |
| `tagQuieting` (basic) | Silences a specific list of tag EPCs from being reported during inventory. Use when you know exactly which tags to suppress. | Reader-scoped |
| `tagQuieting` (advanced) | Uses Gen2 select pre-conditions (mask + state-aware action) to silence tags based on memory content or session state. Use for complex filtering in dense environments. | Reader-scoped |

> Mutually exclusive: only one of `fastID`, `tagProtect`, `tagFocus`, or `tagQuieting` per request. Combining any two returns HTTP 422.

## 5. Choosing TagProtect Actions

TagProtect operations either lock/unlock individual tags or temporarily allow the reader to see already-protected tags. Each action has specific field requirements.

| Action | What It Does | Required Fields | Key Constraints |
|---|---|---|---|
| `enableTagProtection` | Permanently protects a tag; the tag becomes invisible to standard reads until unprotected. | `password`, `tagID` | `password` must be exactly 8 hex characters. Optional `enableShortRange` reduces read range during protection. If omitted, the reader stores `false`. |
| `disableTagProtection` | Removes protection from a previously protected tag, restoring normal visibility. | `password`, `tagID` | `password` must match the tag's existing access password exactly. |
| `enableTagVisibility` | Temporarily allows the reader to read protected tags during this session. Does not change the tag's protection state. | `password` | Reader-scoped; affects all protected tags in field. |
| `disableTagVisibility` | Restores the default behavior where protected tags are hidden from the reader. | `password` | Reverts the effect of `enableTagVisibility`. |

> Important: `enableTagProtection` and `disableTagProtection` are tag-specific (require `tagID`). `enableTagVisibility` and `disableTagVisibility` are reader-wide visibility toggles.

## 6. Choosing TagQuieting Strategy

TagQuieting silences tags from being reported during inventory. Choose between **basic** (EPC-list based) and **advanced** (Gen2 select mask based) depending on your filtering complexity.

### Basic TagQuieting

| Field | What It Controls |
|---|---|
| `action: quiet` | Silences the listed tags from being reported in future inventories. |
| `action: unquiet` | Intended to restore reporting for listed tags. Quieting is session-scoped; starting without `applyImpinjGen2X` is what makes a quieted tag visible again. |
| `tagIDs` | Array of EPCs (hex strings) to quiet or unquiet. Maximum **31 EPCs** per request. |

### Advanced TagQuieting

Advanced quieting uses Gen2 select pre-conditions to silence tags based on memory content and state, instead of explicit EPC lists.

| Field | What It Controls |
|---|---|
| `preSelect[]` | Array of Gen2 select operations applied **before** quieting. Each entry contains `target`, `action`, and `mask`. |
| `preSelect[].target` | The session flag or SL to act upon (`S0`, `S1`, `S2`, `S3`, `SL`). |
| `preSelect[].action` | The state-aware action to take on match/mismatch. SL targets use ASSERTSL / DEASSERTSL / NEGATESL pairs (e.g., `ASSERTSL_NOTHING`, `NEGATESL_NOTHING`). Session targets use INVA / INVB / FLIPAB pairs (e.g., `INVB_INVA`, `FLIPAB_NOTHING`). |
| `preSelect[].mask` | The memory mask: `bank` (EPC/TID/USER/RESERVED), `pointer` (bit offset), `length` (bits), `value` (hex). |
| `tagQuietMasks` | Array of session-flag combinations defining the quieted state (`S0A`, `S2B`, `SL_ASSERT`, `SL_DEASSERT`, etc.). |
| `target` | The target session/flag used for the actual quieting operation. |
| `stateAwareAction` | Same enum as `preSelect[].action` (e.g., `ASSERTSL_DEASSERTSL`, `DEASSERTSL_ASSERTSL`, `NEGATESL_NOTHING`, `FLIPAB_NOTHING`). |

> Important: Use `basic` when you have a discrete list of EPCs. Use `advanced` when filtering by memory content, session state, or complex multi-step Gen2 select conditions.

## 7. Choosing FastID and TagFocus

`fastID` and `tagFocus` each use an `enabled` flag. Neither can be sent in the same request as any other Gen2X feature.

### `fastID`

| Field | What It Controls |
|---|---|
| `enabled: true` | Reader returns EPC + TID together in a single read, reducing total operations. |
| `enabled: false` | Reverts to standard EPC-only reads. |

**Use FastID when:** Your application needs TID for every tag (e.g., authentication, chip-level traceability) and you want to avoid the extra round-trip of a separate TID read.

### `tagFocus`

| Field | What It Controls |
|---|---|
| `enabled: true` | Once a tag is read, it is silenced for the rest of the inventory cycle. The reader focuses only on new tags entering the field. |
| `enabled: false` | Standard inventory behavior; tags can be reported multiple times. |

**Use TagFocus when:** You operate portals, conveyors, or other scenarios with many duplicate reads of the same tag set and want unique-tag reporting.

## 8. Applying the Configuration

Calling this endpoint only **saves** the configuration on the reader; it is not active until inventory is started with the activation flag.

### REST Workflow

```text
PUT  /cloud/stop                 -> stop any active inventory
PUT  /cloud/impinjGen2X          -> save the configuration
GET  /cloud/impinjGen2X          -> verify the saved configuration
PUT  /cloud/start                -> body: { "applyImpinjGen2X": true }
```

### Request Format

Every request to this endpoint follows this structure:

```http
PUT /cloud/impinjGen2X HTTP/1.1
Host: <reader-address>
Authorization: Bearer <token>
Content-Type: application/json

{
  // exactly one Gen2X feature object
}
```

### Success Response (`200 OK`)

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features."
}
```

### Error Responses

| Status Code | Meaning | When It Occurs |
|---|---|---|
| `422 Unprocessable Entity` | Validation error | Empty body, mutually exclusive features sent together, invalid enum value, or constraint violation. |
| `500 Internal Server Error` | Reader-side failure | Internal reader error while persisting the configuration. |

> Persistence: The last saved configuration is kept across reboots. It is applied only for the inventory session started with `applyImpinjGen2X: true`. After `PUT /cloud/stop`, status returns to `feature: none`. A later start without the flag does not re-apply Gen2X.
