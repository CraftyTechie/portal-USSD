from django.db import migrations

def link_transcripts(apps, schema_editor):
    Transcript = apps.get_model('Academic', 'Transcript')
    Student = apps.get_model('Academic', 'Student')

    for transcript in Transcript.objects.all():
        if transcript.student is None:  # Only update if there is no student assigned
            try:
                # Link the student by matching the registration_number
                student = Student.objects.get(registration_number=transcript.student.registration_number)
                transcript.student = student
                transcript.save()
            except Student.DoesNotExist:
                pass  # If no student found, skip this transcript

class Migration(migrations.Migration):

    dependencies = [
        ('Academic', '0003_transcript_student'),  # Update with the last migration name
    ]

    operations = [
        migrations.RunPython(link_transcripts),
    ]
