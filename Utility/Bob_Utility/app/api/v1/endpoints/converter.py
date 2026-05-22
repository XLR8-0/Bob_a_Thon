"""
Converter Tools API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict

from app.core.exceptions import ValidationError, ProcessingError
from app.services.xml.converter import XMLConverter
from app.services.text_converter import TextConverter
from app.services.csv_converter import CSVConverter

router = APIRouter(prefix="/converter", tags=["Converter Tools"])


# Request/Response Models
class XMLToJSONConvertRequest(BaseModel):
    xml_content: str = Field(..., description="XML content to convert")
    pretty: bool = Field(True, description="Pretty print JSON")
    indent: int = Field(2, description="Indentation spaces")
    use_sample: bool = Field(False, description="Use sample data instead")


class JSONToXMLConvertRequest(BaseModel):
    json_content: str = Field(..., description="JSON content to convert")
    root_tag: str = Field("root", description="Root element tag name")
    pretty: bool = Field(True, description="Pretty print XML")
    indent: int = Field(2, description="Indentation spaces")
    use_sample: bool = Field(False, description="Use sample data instead")


class JSONToCSVConvertRequest(BaseModel):
    json_content: str = Field(..., description="JSON content to convert (array of objects)")
    delimiter: str = Field(",", description="CSV delimiter")
    include_header: bool = Field(True, description="Include header row")
    use_sample: bool = Field(False, description="Use sample data instead")


class CSVToJSONConvertRequest(BaseModel):
    csv_content: str = Field(..., description="CSV content to convert")
    delimiter: str = Field(",", description="CSV delimiter")
    pretty: bool = Field(True, description="Pretty print JSON")
    indent: int = Field(2, description="Indentation spaces")
    use_sample: bool = Field(False, description="Use sample data instead")


class ConvertResponse(BaseModel):
    success: bool
    result: str
    message: Optional[str] = None


class SampleDataResponse(BaseModel):
    success: bool
    sample_data: str
    format: str


# XML to JSON Converter
@router.post("/xml-to-json", response_model=ConvertResponse)
async def convert_xml_to_json(request: XMLToJSONConvertRequest) -> ConvertResponse:
    """Convert XML to JSON"""
    try:
        converter = XMLConverter()
        
        # Use sample data if requested
        if request.use_sample:
            xml_content = converter.get_sample_xml()
        else:
            xml_content = request.xml_content
        
        if not xml_content or not xml_content.strip():
            raise ValidationError("XML content is required")
        
        result = converter.xml_to_json(
            xml_content=xml_content,
            pretty=request.pretty,
            indent=request.indent
        )
        
        return ConvertResponse(
            success=True,
            result=result,
            message="Successfully converted XML to JSON"
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


# JSON to XML Converter
@router.post("/json-to-xml", response_model=ConvertResponse)
async def convert_json_to_xml(request: JSONToXMLConvertRequest) -> ConvertResponse:
    """Convert JSON to XML"""
    try:
        converter = XMLConverter()
        csv_converter = CSVConverter()
        
        # Use sample data if requested
        if request.use_sample:
            json_content = csv_converter.get_sample_json()
        else:
            json_content = request.json_content
        
        if not json_content or not json_content.strip():
            raise ValidationError("JSON content is required")
        
        result = converter.json_to_xml(
            json_content=json_content,
            root_tag=request.root_tag,
            pretty=request.pretty,
            indent=request.indent
        )
        
        return ConvertResponse(
            success=True,
            result=result,
            message="Successfully converted JSON to XML"
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


# JSON to CSV Converter
@router.post("/json-to-csv", response_model=ConvertResponse)
async def convert_json_to_csv(request: JSONToCSVConvertRequest) -> ConvertResponse:
    """Convert JSON to CSV"""
    try:
        converter = CSVConverter()
        
        # Use sample data if requested
        if request.use_sample:
            json_content = converter.get_sample_json()
        else:
            json_content = request.json_content
        
        if not json_content or not json_content.strip():
            raise ValidationError("JSON content is required")
        
        result = converter.json_to_csv(
            json_content=json_content,
            delimiter=request.delimiter,
            include_header=request.include_header
        )
        
        return ConvertResponse(
            success=True,
            result=result,
            message="Successfully converted JSON to CSV"
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


# CSV to JSON Converter
@router.post("/csv-to-json", response_model=ConvertResponse)
async def convert_csv_to_json(request: CSVToJSONConvertRequest) -> ConvertResponse:
    """Convert CSV to JSON"""
    try:
        converter = CSVConverter()
        
        # Use sample data if requested
        if request.use_sample:
            csv_content = converter.get_sample_csv()
        else:
            csv_content = request.csv_content
        
        if not csv_content or not csv_content.strip():
            raise ValidationError("CSV content is required")
        
        result = converter.csv_to_json(
            csv_content=csv_content,
            delimiter=request.delimiter,
            pretty=request.pretty,
            indent=request.indent
        )
        
        return ConvertResponse(
            success=True,
            result=result,
            message="Successfully converted CSV to JSON"
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


# Get Sample Data
@router.get("/sample/{format}", response_model=SampleDataResponse)
async def get_sample_data(format: str) -> SampleDataResponse:
    """Get sample data for testing converters"""
    try:
        xml_converter = XMLConverter()
        csv_converter = CSVConverter()
        
        if format.lower() == "xml":
            return SampleDataResponse(
                success=True,
                sample_data=xml_converter.get_sample_xml(),
                format="xml"
            )
        elif format.lower() == "json":
            return SampleDataResponse(
                success=True,
                sample_data=csv_converter.get_sample_json(),
                format="json"
            )
        elif format.lower() == "csv":
            return SampleDataResponse(
                success=True,
                sample_data=csv_converter.get_sample_csv(),
                format="csv"
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown format: {format}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sample data: {str(e)}")

# Text Case Converter Models
class TextCaseConvertRequest(BaseModel):
    text_content: str = Field(..., description="Text content to convert")
    case_type: str = Field(..., description="Case type: lower, upper, or proper")


class TextCaseConvertResponse(BaseModel):
    success: bool
    converted_text: str
    statistics: Dict[str, int]
    case_type: str
    message: Optional[str] = None


# Text Case Converter
@router.post("/change-case", response_model=TextCaseConvertResponse)
async def change_text_case(request: TextCaseConvertRequest) -> TextCaseConvertResponse:
    """Convert text case (lower, upper, proper) and return statistics"""
    try:
        converter = TextConverter()
        
        if not request.text_content or not request.text_content.strip():
            raise ValidationError("Text content is required")
        
        result = converter.convert_case(
            text=request.text_content,
            case_type=request.case_type
        )
        
        return TextCaseConvertResponse(
            success=True,
            converted_text=result["converted_text"],
            statistics=result["statistics"],
            case_type=result["case_type"],
            message=f"Successfully converted text to {result['case_type']} case"
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Case conversion failed: {str(e)}")


# Get Text Statistics
@router.post("/text-statistics")
async def get_text_statistics(request: TextCaseConvertRequest):
    """Get text statistics without conversion"""
    try:
        converter = TextConverter()
        
        if not request.text_content:
            raise ValidationError("Text content is required")
        
        stats = converter.get_text_statistics(request.text_content)
        
        return {
            "success": True,
            "statistics": stats,
            "message": "Successfully calculated text statistics"
        }
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics calculation failed: {str(e)}")



# Made with Bob