from contact.models import Contact
from contact.serializers import ContactSerializer
from rest_framework import generics
from rest_framework.response import Response


class ContactListView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        step_user = request.data.get('step_user', None)
        if step_user is None:
            return Response(data={'messages': 'step_user is need for get contact list.'}, status=400)

        queryset = Contact.objects.filter(step_user=step_user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

