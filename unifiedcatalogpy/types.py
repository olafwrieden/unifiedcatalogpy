from enum import Enum


class GovernanceDomainType(str, Enum):
    FunctionalUnit = "FunctionalUnit"
    LineOfBusiness = "LineOfBusiness"
    DataDomain = "DataDomain"
    Regulatory = "Regulatory"
    Project = "Project"


class GovernanceDomainStatus(str, Enum):
    Draft = "Draft"
    Published = "Published"


class TermStatus(str, Enum):
    Draft = "Draft"
    Published = "Published"
    Archived = "Expired"


class RelationshipType(str, Enum):
    Synonym = "Synonym"
    Related = "Related"


class RelationshipEntityType(str, Enum):
    Term = "Term"
    DataProduct = "DataProduct"
    CriticalDataElement = "CriticalDataElement"
    CustomMetadata = "CustomMetadata"


class DataProductStatus(str, Enum):
    Draft = "Draft"
    Published = "Published"
    Expired = "Expired"


class DataProductType(str, Enum):
    Dataset = "Dataset"
    MasterDataAndReferenceData = "MasterDataAndReferenceData"
    BusinessSystemOrApplication = "BusinessSystemOrApplication"
    ModelTypes = "ModelTypes"
    DashboardsOrReports = "DashboardsOrReports"
    Operational = "Operational"


class DataProductUpdateFrequency(str, Enum):
    Hourly = "Hourly"
    Daily = "Daily"
    Weekly = "Weekly"
    Monthly = "Monthly"
    Quarterly = "Quarterly"
    Yearly = "Yearly"


class AudienceType(str, Enum):
    DataEngineer = "DataEngineer"
    BIEngineer = "BIEngineer"
    DataAnalyst = "DataAnalyst"
    DataScientist = "DataScientist"
    BusinessAnalyst = "BusinessAnalyst"
    SoftwareEngineer = "SoftwareEngineer"
    BusinessUser = "BusinessUser"
    Executive = "Executive"


class ObjectiveStatus(str, Enum):
    Draft = "Draft"
    Published = "Published"
    Closed = "Closed"


class CriticalDataElementStatus(str, Enum):
    Draft = "Draft"
    Published = "Published"
    Expired = "Expired"


class CriticalDataElementDataType(str, Enum):
    Number = "Number"
    Text = "Text"
    DateTime = "DateTime"
    Boolean = "Boolean"


class KeyResultStatus(str, Enum):
    Behind = "Behind"
    OnTrack = "OnTrack"
    AtRisk = "AtRisk"


class HealthActionStatus(str, Enum):
    NotStarted = "NotStarted"
    InProgress = "InProgress"
    Resolved = "Resolved"


class HealthActionCategory(str, Enum):
    HealthControl = "HealthControl"


class HealthActionSeverity(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class HealthControlScheduleStatus(str, Enum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class HealthControlFrequency(str, Enum):
    Day = "Day"
    Week = "Week"
    Month = "Month"
