import json
import urllib

from auth_server.auth import verify_user

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from auth_server.lambda_typing import LambdaDict, LambdaContext


def lambda_handler(event: "LambdaDict", context: "LambdaContext") -> "LambdaDict":
    body = event.get("body")

    if body:
        form_data = {
            entry.split("=")[0]: entry.split("=")[-1] for entry in body.split("&")
        }

        user_id = verify_user(
            urllib.parse.unquote(form_data.get("user_email", "")),
            form_data.get("password", ""),
            form_data.get("mfa_code", ""),
        )

        if user_id:
            return {
                "statusCode": 200,
                "body": json.dumps({"user_id": user_id,}),
            }

    return {
        "statusCode": 403,
        "body": json.dumps({}),
    }
