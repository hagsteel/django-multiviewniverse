Multiviewniverse (alpha)
========================

Multiple django models and forms in one view


Create view
-----------
When using create, the view will update the forms initials, to contain possible models for use with foreign keys

```
class CreatePersonPetView(MultiModelCreateFormView):
    model_form_classes = [(PetForm, Pet), (PersonForm, Person)]
    template_name = 'person_pet_form.html'
    success_url = '/'
```

In the demo, the person is supplied to the pet as an unsaved model (i.e it has no primary key).
At this point you have to manually save the model (as there is no way of knowing if these models are related or not).

```
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
```


Update view
-----------
Notice that in an update view you need to implement get_[model name]_object() to be able to get the instance
of the object you are updating

```
class UpdatePersonPetView(MultiModelUpdateFormView):
    model_form_classes = [(PersonForm, Person), (PetForm, Pet)]
    template_name = 'person_pet_form.html'
    success_url = '/'

    def get_person_object(self):
        return Person.objects.get(pk=self.kwargs['person_pk'])

    def get_pet_object(self):
        return self.get_person_object().pets.get(pk=self.kwargs['pet_pk'])

```