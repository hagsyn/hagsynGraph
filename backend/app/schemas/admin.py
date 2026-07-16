from pydantic import BaseModel, Field


class StoragePolicy(BaseModel):
    autoCleanupEnabled: bool = True
    uploadRetentionHours: int = Field(default=72, ge=1, le=24 * 90)
    compressedRetentionHours: int = Field(default=168, ge=1, le=24 * 180)
    subtitleRetentionHours: int = Field(default=168, ge=1, le=24 * 180)
    toolRunRetentionHours: int = Field(default=24 * 30, ge=1, le=24 * 365)
    deleteIntermediateAudio: bool = True
    cleanupFailedTemporaryFiles: bool = True


class StoragePolicyResponse(BaseModel):
    isAdmin: bool
    policy: StoragePolicy


class CleanupResult(BaseModel):
    filesDeleted: int
    bytesFreed: int
    toolRunsDeleted: int
    directories: list[str]
