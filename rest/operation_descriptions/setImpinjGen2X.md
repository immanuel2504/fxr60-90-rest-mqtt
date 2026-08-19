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
| Supported Tag Quiet Masks | S0A, S0B, S1A, S1B, S2A, S2B, S3A, S3B, SL_ASSERT, SL_DEASSERT |
| Mutually Exclusive Features | `fastID`, `tagFocus`, `tagQuieting` (only one reader-scoped feature active at a time) |

## 3. Before You Begin

Decide which Gen2X feature to configure before sending this request. At least one feature object must be included in the request body, but mutually exclusive reader-scoped features cannot be combined in a single request. To apply the saved Gen2X configuration during inventory, send `PUT /cloud/start` with `applyImpinjGen2X: true`.

| What You Need | Details |
|---|---|
| Feature selection | At least one of `fastID`, `tagProtect`, `tagFocus`, or `tagQuieting` must be present - an empty request body will be rejected. Choose only one reader-scoped feature (`fastID`, `tagFocus`, or `tagQuieting`) per request; `tagProtect` is tag-scoped and can be configured independently. |
| FastID | Decide whether to enable or disable TID embedding. Optionally specify a TID word selector (`TID[0]`-`TID[3]`). |
| TagProtect action | Choose one of: `enableTagProtection` (protect a specific tag), `disableTagProtection` (remove protection from a tag), `enableTagVisibility` (allow reading protected tags), `disableTagVisibility` (block reading protected tags). |
| TagProtect password | An 8-character hex string (32-bit) is required for all TagProtect actions. |
| TagProtect tag EPC | `tagID` (hex EPC) is required for `enableTagProtection` and `disableTagProtection`. It must be omitted for `enableTagVisibility` and `disableTagVisibility`. |
| TagFocus | Whether to enable or disable the feature. TagFocus targets session S1. |
| TagQuieting | For basic: provide `action` (`quiet`/`unquiet`) and the `tagIDs` EPC array (maximum 31 tag IDs per request). For advanced: provide the `preSelect` array, `tagQuietMasks`, `target`, and `stateAwareAction`. |
| Inventory state | Configure Gen2X before starting inventory. Stop any active inventory first with `PUT /cloud/stop`. |
| Activation | Gen2X settings are saved but not applied until `PUT /cloud/start` is sent with `applyImpinjGen2X: true`. |

## 4. Choosing a Gen2X Feature

The Gen2X feature you select determines the reader's behavior during inventory. Choose based on your operational goal.

| Feature | Description | Scope |
|---|---|---|
| `fastID` | Returns the EPC and TID together in a single read, eliminating the need for a separate TID read. Best for applications that require chip-level identity (anti-counterfeit, authentication). | Reader-scoped |
| `tagProtect` | Password-protects individual tags or controls reader visibility of protected tags. Use for securing sensitive items or restricting access. | Tag-scoped |
| `tagFocus` | Silences already-read tags so the reader focuses only on new tags entering the field. Ideal for portal and conveyor applications. | Reader-scoped |
| `tagQuieting` (basic) | Silences a specific list of tag EPCs from being reported during inventory. Use when you know exactly which tags to suppress. | Reader-scoped |
| `tagQuieting` (advanced) | Uses Gen2 select pre-conditions (mask + state-aware action) to silence tags based on memory content or session state. Use for complex filtering in dense environments. | Reader-scoped |

> Mutually exclusive: Only one of `fastID`, `tagFocus`, or `tagQuieting` can be active at a time. `tagProtect` can coexist with any one of them because it operates at the tag level.

## 5. Choosing TagProtect Actions

TagProtect operations either lock/unlock individual tags or temporarily allow the reader to see already-protected tags. Each action has specific field requirements.

| Action | What It Does | Required Fields | Key Constraints |
|---|---|---|---|
| `enableTagProtection` | Permanently protects a tag; the tag becomes invisible to standard reads until unprotected. | `password`, `tagID` | `password` must be exactly 8 hex characters. Optional `enableShortRange` reduces read range during protection. |
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
| `action: unquiet` | Restores reporting for previously quieted tags. |
| `tagIDs` | Array of EPCs (hex strings) to quiet or unquiet. Maximum **31 EPCs** per request. |

### Advanced TagQuieting

Advanced quieting uses Gen2 select pre-conditions to silence tags based on memory content and state, instead of explicit EPC lists.

| Field | What It Controls |
|---|---|
| `preSelect[]` | Array of Gen2 select operations applied **before** quieting. Each entry contains `target`, `action`, and `mask`. |
| `preSelect[].target` | The session flag or SL to act upon (`S0`, `S1`, `S2`, `S3`, `SL`). |
| `preSelect[].action` | The state-aware action to take on match/mismatch (e.g., `ASSERTSL_NOTHING`, `INVB_INVA`, `DEASSERTSL_NOTHING`, `INVA_INVB`). |
| `preSelect[].mask` | The memory mask: `bank` (EPC/TID/USER/RESERVED), `pointer` (bit offset), `length` (bits), `value` (hex). |
| `tagQuietMasks` | Array of session-flag combinations defining the quieted state (`S0A`, `S2B`, `SL_ASSERT`, `SL_DEASSERT`, etc.). |
| `target` | The target session/flag used for the actual quieting operation. |
| `stateAwareAction` | The compound state action (e.g., `ASSERTSL_DEASSERTSL`, `DEASSERTSL_ASSERTSL`) applied during quieting. |

> Important: Use `basic` when you have a discrete list of EPCs. Use `advanced` when filtering by memory content, session state, or complex multi-step Gen2 select conditions.

## 7. Choosing FastID and TagFocus

These two reader-scoped features improve inventory performance but cannot be combined.

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
  // one or more Gen2X feature objects
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

> Persistence: The reader stores the last saved configuration and restores it across reboots and reconnects. The configuration is only applied during inventory when `applyImpinjGen2X: true` is sent in the `PUT /cloud/start` request body.
