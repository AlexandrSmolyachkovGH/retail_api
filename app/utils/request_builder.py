import json

from pydantic import BaseModel

from app.settings.retailcrm_settings import (
    retail_crm_settings,
)


class RequestBuilder:
    def process_scheme(
        self,
        scheme: BaseModel,
        exclude_none: bool = True,
        exclude_defaults: bool = False,
        exclude_unset: bool = False,
    ) -> dict:
        scheme_data = scheme.model_dump(
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            exclude_unset=exclude_unset,
        )
        return scheme_data

    def build_filter_params(
        self,
        processed_scheme: dict,
    ) -> dict:
        params = {
            "apiKey": retail_crm_settings.api_key,
        }
        if processed_scheme:
            for k, v in processed_scheme.items():
                if k not in ["limit", "page"]:
                    k = f"filter[{k}]"
                params[k] = v
        return params

    def build_body(
        self,
        processed_scheme: dict,
        field_name: str,
        simple_field: bool = True,
        extra_data: dict[str, str] | None = None,
    ) -> dict:
        """Create a body for RetailCRM requests"""
        data = (
            json.dumps(processed_scheme) if simple_field else processed_scheme
        )
        body = {
            "apiKey": retail_crm_settings.api_key,
            field_name: data,
        }
        if extra_data:
            body.update(extra_data)
        return body


builder = RequestBuilder()
