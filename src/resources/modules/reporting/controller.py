from typing import Dict, Type

from flask_restful import Resource

from .report_phishing import ReportIncidentService
from .get_analysis import GetAnalysisService

reporting_factory: Dict[str, Type[Resource]] = {
    "/v1/report/phishing": ReportIncidentService,
    "/v1/analysis/phishing": GetAnalysisService,
}
   