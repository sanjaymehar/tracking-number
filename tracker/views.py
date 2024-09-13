from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import TrackingNumber
from .serializers import TrackingNumberSerializer
import uuid
import random
import string
from datetime import datetime
from django.db import IntegrityError, transaction
from rest_framework import status
from dateutil.parser import isoparse
from django.db import IntegrityError
from django.core.exceptions import ValidationError


# Random tracking number
def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))


# Generating a unique tracking number
def generate_unique_tracking_number():

    for _ in range(5):
        tracking_number = generate_tracking_number()
        try:
            with transaction.atomic():

                if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                    return tracking_number
        except IntegrityError:
            # If there's an IntegrityError, retry the operation
            continue
    raise IntegrityError('Failed to generate a unique tracking number after multiple attempts.')


@api_view(['GET'])
def generate_tracking_number_view(request):
    # Required parameters
    required_params = {
        'origin_country_id': request.GET.get('origin_country_id'),
        'destination_country_id': request.GET.get('destination_country_id'),
        'weight': request.GET.get('weight'),
        'created_at': request.GET.get('created_at'),
        'customer_id': request.GET.get('customer_id'),
        'customer_name': request.GET.get('customer_name'),
        'customer_slug': request.GET.get('customer_slug')
    }

    # Checking for missing parameters
    missing_params = [param for param, value in required_params.items() if not value]

    if missing_params:
        return Response({'error': f'Missing required parameters: {", ".join(missing_params)}.'}, status=status.HTTP_400_BAD_REQUEST)

    # Extracting parameters
    origin_country_id = required_params['origin_country_id']
    destination_country_id = required_params['destination_country_id']
    weight = required_params['weight']
    created_at = required_params['created_at']
    customer_id = required_params['customer_id']
    customer_name = required_params['customer_name']
    customer_slug = required_params['customer_slug']

    # Validate the created_at parameter
    try:
        created_at_timestamp = isoparse(created_at)
    except ValueError:
        return Response({'error': 'Invalid created_at format. Use RFC 3339 format.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate weight
    try:
        weight = float(weight)
        if weight <= 0:
            return Response({'error': 'Weight must be a positive number.'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid weight format.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate customer_id
    try:
        customer_id = uuid.UUID(customer_id)
    except ValueError:
        return Response({'error': 'Invalid customer_id format. Must be a valid UUID.'}, status=status.HTTP_400_BAD_REQUEST)

    # Generating a unique tracking number
    try:
        tracking_number = generate_unique_tracking_number()
    except IntegrityError:
        return Response({'error': 'Failed to generate a unique tracking number.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    try:
        tracking = TrackingNumber(
            tracking_number=tracking_number,
            origin_country_id=origin_country_id,
            destination_country_id=destination_country_id,
            weight=weight,
            created_at_timestamp=created_at_timestamp,
            customer_id=customer_id,
            customer_name=customer_name,
            customer_slug=customer_slug
        )
        tracking.save()
    except ValidationError as e:
        return Response({'error': f'Validation error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


    response_data = {
        'tracking_number': tracking_number,
        'created_at': created_at_timestamp.replace(microsecond=0).isoformat()
    }
    return Response(response_data)

