from fastapi.responses import JSONResponse


def success_response(
    data,
    *,
    status_code: int = 200,
    meta: dict | None = None,
    message: str | None = None,
) -> JSONResponse:
    """
    Standard success envelope.

    Shape:
    {
        "success": true,
        "data": <data>,
        "message": <optional message>,
        "meta": <optional meta>
    }
    """
    content: dict = {"success": True, "data": data}

    if message is not None:
        content["message"] = message

    if meta is not None:
        content["meta"] = meta

    return JSONResponse(status_code=status_code, content=content)
