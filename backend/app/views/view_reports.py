import asyncio
from backend.settings import log
from app.models import Task, Reminder
from django.utils.timezone import now
from app.ai.vertex_ai_agent import agent
from rest_framework.views import APIView
from app.serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ReportView(APIView):
    """
    API endpoint to generate AI-powered daily task reports for the logged-in user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Generate a daily report based on the user's tasks."""
        # Fetch only today's tasks for the logged-in user
        tasks = Task.objects.filter(
            client=request.user, due_date__date=now().date()
        ).order_by("due_date")

        serializer = TaskSerializer(tasks, many=True)
        from app.ai.marvin_ai_agent import summarize_tasks_by_priority

        log.info("serializer.data", serializer=serializer.data)

        return Response(summarize_tasks_by_priority(serializer.data), status=200)


class PriorityTaskView(APIView):
    """
    API endpoint to generate AI-powered daily priority tasks.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Generate a summary of high-priority tasks."""
        tasks = Task.objects.filter(
            client=request.user, priority="high", due_date__date=now().date()
        ).order_by("due_date")

        if not tasks.exists():
            return Response(
                {"message": "No high-priority tasks for today."}, status=200
            )

        task_data = "\n".join(
            [
                f"- {task.title} (Due: {task.due_date.strftime('%I:%M %p')})"
                for task in tasks
            ]
        )

        prompt = f"Summarize today's high-priority tasks:\n{task_data}"
        return Response({"priority_tasks": agent.run_sync(prompt).data}, status=200)


class ClientReminderView(APIView):
    """
    API endpoint to schedule client reminders.
    """

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """Generate reminders for client-related events like birthdays and follow-ups."""

        # Get reminders for the user
        # -------------------------------------------------------
        reminders = Reminder.objects.filter(
            client=request.user, reminder_time__date=now().date()
        ).order_by("reminder_time")

        # Generate a prompt for the user based on time
        # -------------------------------------------------------
        reminder_data = "\n".join(
            [
                f"- {reminder.task.title} at {reminder.reminder_time.strftime('%I:%M %p')}"
                for reminder in reminders
            ]
        )
        prompt = f"Generate a summary of today's client reminders:\n{reminder_data}"

        # Ensure an event loop exists in this thread
        # -------------------------------------------------------
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run AI processing asynchronously
        # -------------------------------------------------------
        response = loop.run_until_complete(agent.run(prompt))
        return Response({"client_reminders": response.data}, status=200)


class AdvisorQuerySuggestionView(APIView):
    """
    API endpoint to suggest useful queries for financial advisors.
    """

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """Generate AI-powered query suggestions for financial advisors."""
        prompt = """
        Suggest useful queries a financial advisor might find helpful for market trends, 
        client investments, and risk assessment.
        """
        # Ensure an event loop exists in this thread
        # -------------------------------------------------------
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run AI processing asynchronously
        # -------------------------------------------------------
        response = loop.run_until_complete(agent.run(prompt))
        return Response({"advisor_queries": response.data}, status=200)
