class AlertPriority:
    DEFAULT = {
        "LOW": "LOW",
        "MEDIUM": "MEDIUM",
        "HIGH": "HIGH",
        "CRITICAL": "CRITICAL"
    }

    @classmethod
    def from_severity(cls, severity: str) -> str:
        return cls.DEFAULT.get(severity.upper(), "LOW")