class TitleMixin(object):
    title = 'Neighbourhood'
    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
class ListMixin(object):
    title = 'Neighbourhood - Список'
    def get_context_data(self, **kwargs):
        context = super(ListMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context