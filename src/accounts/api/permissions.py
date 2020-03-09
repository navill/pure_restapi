from rest_framework import permissions


# class BlacklistPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blacklisted

# register에서 사용될 permission
# token을 가지고 가입할 경우 {'detail': '로그아웃 이후 다시 시도해주세요.'}
# view level
class AnonPermissionOnly(permissions.BasePermission):
    message = '로그아웃 이후 다시 시도해주세요.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


# object level
class IsOwnerOrReadOnly(permissions.BasePermission):
    message = '객체에 대한 권한을 가지고 있지 않습니다.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
