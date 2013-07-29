from django import forms

class UploadForm( forms.Form ):
    # Title
    # Draft
    # File
    title = forms.CharField(  )
    draft_number = forms.IntegerField( min_value = 1,
                                help_text="e.g. 1 for first draft, 2 for second draft", error_messages={ 'invalid' : "You must provide a numeric draft number, use 1 if this is the only draft." } )
    script = forms.FileField( label="Script Filename")
