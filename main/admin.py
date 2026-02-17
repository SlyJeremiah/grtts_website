# ===== FIXED APPLICANTPROFILE ADMIN =====
@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'get_full_name', 'get_user_phone', 'created_at']  # Changed 'phone' to 'get_user_phone'
    list_filter = ['gender', 'nationality', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'user__phone']  # Search in user model
    readonly_fields = ['created_at', 'updated_at']
    
    def user_email(self, obj):
        return obj.user.email if obj.user else "No user"
    user_email.short_description = "Email"
    
    def get_full_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return "No user"
    get_full_name.short_description = "Full Name"
    
    def get_user_phone(self, obj):  # New method to get phone from user
        return obj.user.phone if obj.user and obj.user.phone else "No phone"
    get_user_phone.short_description = "Phone"
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'nationality')
        }),
        ('Address', {
            'fields': ('address', 'city', 'province')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_name', 'emergency_phone', 'emergency_relationship')
        }),
        ('Health', {
            'fields': ('medical_conditions', 'dietary_requirements')
        }),
        ('Documents', {
            'fields': ('id_document', 'cv', 'certificates'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
