def upgrade_artifacts(artifacts_data):
    for artifacts_piece in artifacts_data.values():
        for artifact in artifacts_piece:
            artifact['level'] = 20
