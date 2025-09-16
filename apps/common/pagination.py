from django.core.paginator import Paginator
from django.db.models import QuerySet

from .responses import APIResponse


class PaginationUtility:
    @staticmethod
    def paginated(
        queryset: QuerySet,
        page: int,
        per_page: int,
        serializer_class=None,
        serializer_context: dict | None = None,
        message: str = "Data retrieved successfully",
    ):
        """
        Paginated response with comprehensive metadata.

        Args:
            queryset: Django QuerySet to paginate
            page: Current page number
            per_page: Items per page
            serializer_class: DRF serializer for data transformation
            serializer_context: Context for serializer
            message: Success message

        Returns:
            Paginated response with metadata
        """
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        # Serialize data if serializer provided
        if serializer_class and page_obj.object_list:
            serializer = serializer_class(
                page_obj.object_list, many=True, context=serializer_context or {}
            )
            data = serializer.data
        else:
            data = (
                list(page_obj.object_list.values())
                if hasattr(page_obj.object_list, "values")
                else list(page_obj.object_list)
            )

        metadata = {
            "pagination": {
                "total_items": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "per_page": per_page,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
                "next_page": page_obj.next_page_number()
                if page_obj.has_next()
                else None,
                "previous_page": page_obj.previous_page_number()
                if page_obj.has_previous()
                else None,
                "items_on_page": len(data),
            }
        }
        return APIResponse.success(data=data, message=message, metadata=metadata)
