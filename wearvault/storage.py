from whitenoise.storage import CompressedManifestStaticFilesStorage, MissingFileError


class IgnoreMissingManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

    def post_process(self, *args, **kwargs):
        processed = super().post_process(*args, **kwargs)
        try:
            for item in processed:
                yield item
        except MissingFileError:
            # Ignore missing referenced files (e.g., absent sourcemaps)
            return


