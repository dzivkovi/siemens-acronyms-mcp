# Simple API Root Redirect to Documentation

## Problem / Metric

FastAPI services generate empty landing pages at the root URL (/), causing confusion for internal users who don't know about `/docs` endpoint. Internal API users need immediate access to interactive documentation without extra clicks or confusion.

**Metric**: Eliminate user confusion and provide instant access to Swagger documentation for internal APIs.

## Goal

Implement a simple redirect from the root URL (/) directly to the FastAPI Swagger documentation (/docs), providing zero-maintenance instant access to interactive API documentation.

## Scope (M/S/W)

- [M] Redirect root URL (/) to /docs endpoint
- [M] Use HTTP 307 (Temporary Redirect) status code
- [M] Zero maintenance solution requiring no ongoing updates
- [S] Preserve any query parameters in redirect
- [W] Landing page content or HTML responses
- [W] README display or custom styling
- [W] Multiple documentation endpoint options

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | FastAPI app is running | User visits / | User redirects to /docs immediately |
| 2 | User visits / with query params | User visits /?param=value | User redirects to /docs with params preserved |
| 3 | FastAPI app is running | User visits /docs directly | Swagger UI loads normally |
| 4 | Redirect is implemented | User bookmarks / | Bookmark works and redirects to /docs |

## Technical Design

Implement a single FastAPI route handler for the root path (/) that returns a RedirectResponse to the /docs endpoint.

**Key Components**:

1. **Route Handler**: Simple GET endpoint at root path
2. **Redirect Response**: FastAPI's built-in RedirectResponse class
3. **Target URL**: Hard-coded "/docs" path (FastAPI's default Swagger endpoint)

**Architecture Decision**: Use RedirectResponse instead of HTMLResponse for maximum simplicity and browser compatibility. This approach requires zero maintenance and leverages FastAPI's existing documentation infrastructure.

**Status Code**: Use default redirect behavior (307 Temporary Redirect) to indicate this is a routing convenience, not a permanent URL structure change.

## Implementation Steps

1. Import `RedirectResponse` from `fastapi.responses`
2. Create GET route handler for root path: `@app.get("/")`
3. Return `RedirectResponse(url="/docs")` from the handler
4. Test redirect functionality in browser
5. Verify existing /docs endpoint still works independently

## Testing Strategy

**Manual Testing**:

- Navigate to root URL in browser - verify immediate redirect to /docs
- Test with query parameters - verify params are preserved
- Test direct /docs access - verify Swagger UI loads normally
- Test in different browsers for compatibility
- Verify no console errors or redirect loops

**Functional Verification**:

- Confirm single redirect hop (no multiple redirects)
- Verify HTTP status code is 307 (Temporary Redirect)
- Test that existing API endpoints remain unaffected

## Risks & Considerations

**Browser Compatibility**: RedirectResponse is universally supported across all modern browsers.

**Performance**: Single redirect adds minimal latency (~1-5ms) and is cached by browsers.

**Maintenance**: Truly zero maintenance - no files to update, no content to maintain.

**Future Flexibility**: If landing page needs arise later, simply replace redirect with HTML response.

**User Experience**: Internal users get immediate access to interactive documentation without learning about /docs endpoint.
