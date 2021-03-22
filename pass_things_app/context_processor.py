from .forms import ContactForm


def context_proc(request):
    contact_form = ContactForm(auto_id=False, )
    ctx = {
        'contact_form': contact_form,
    }
    return ctx
