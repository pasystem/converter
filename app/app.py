import logging

import base64
import pdfkit
from pydantic import BaseModel, Field
from fastapi import FastAPI
from starlette.responses import Response

from config import settings

logger = logging.getLogger(__name__)

app = FastAPI()

pdf_config = pdfkit.configuration(
    wkhtmltopdf=settings.wkhtmltopdf,
)


class SourceData(BaseModel):
    source: bytes
    filename: str = Field(default='output.pdf')


@app.post("/convert")
def convert(data: SourceData):
    """html to pdf file conversion service"""
    try:
        pdf = pdfkit.from_string(
            base64.b64decode(data.source).decode(),
            configuration=pdf_config
        )

        return Response(
            pdf,
            headers={
                "Content-Type": "application/pdf",
                "Content-Disposition": f"attachment; filename={data.filename}",
                "Content-Length": str(len(pdf)),
            },
        )

    except Exception as exc:
        logger.error("convert error %s", exc)
        raise exc
