from rest_framework import permissions


class DepartmentStaffOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Model-level permission
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            # SAFE_METHODS(e.g.GET) is granted for both authenticated and non-authenticated users.
            # Other Methods are granted only for authenticated users.
            return True

        else:
            # only staff who belongs to an department can create product.
            if request.user.is_authenticated:
                if request.user.is_staff and request.user.department:
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        """
           Object-level permission.
           Return `True` if permission is granted, `False` otherwise.
        """
        # SAFE_METHODS(e.g.GET) is granted for all users.
        # Other Methods are granted only for owner.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the staff who is from the department that has access to maintain the product
        else:
            return obj.category == request.user.department.category


class DepartmentStaffOnly2(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Model-level permission
        Return `True` if permission is granted, `False` otherwise.
        """

        if request.user.is_authenticated:
            if request.user.is_staff and request.user.department:
                return True
        return False
