from django import forms
from .models import Pet, Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ('owner',)

    def save(self, commit=True):
        if (commit):
            if 'person' in self.initial:
                if not self.initial['person'].pk:
                    self.initial['person'].save()
                self.instance.owner = self.initial['person']
            return super(PetForm, self).save(commit)
        return super(PetForm, self).save(commit)