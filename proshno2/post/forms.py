from django import forms
from post.models import Post, PostComment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model= Post
        fields= '__all__'
        exclude = ('author',)



class CommentCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = '__all__'

        exclude = ('author', 'post', 'down_vote', 'up_vote')

    def __init__(self, *args, **kwargs):
        super(CommentCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "Write a Comment"
