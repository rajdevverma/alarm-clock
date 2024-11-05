import time
import subprocess
from plyer import notification
import pygame

# Initialize pygame mixer for playing sound
pygame.mixer.init()

class LinuxAlarmClock:
    def __init__(self):
        self.alarms = []

    def set_alarm(self, alarm_time, sound_file=None, message=None, command=None):
        """
        Set an alarm with a specific time, sound, message, or command.
        
        :param alarm_time: The time at which the alarm should go off (24-hour format: HH:MM)
        :param sound_file: Path to a sound file (optional)
        :param message: Message to display in the notification (optional)
        :param command: Command to run when the alarm goes off (optional)
        """
        alarm = {
            'alarm_time': alarm_time,
            'sound_file': sound_file,
            'message': message,
            'command': command
        }
        self.alarms.append(alarm)
        print(f"Alarm set for {alarm_time}")

    def check_alarms(self):
        """
        Check if any alarm should go off based on the current time.
        """
        while True:
            current_time = time.strftime('%H:%M')
            for alarm in self.alarms:
                if alarm['alarm_time'] == current_time:
                    self.trigger_alarm(alarm)
                    self.alarms.remove(alarm)
            time.sleep(60)  # Check every minute

    def trigger_alarm(self, alarm):
        """
        Trigger the alarm: play sound, show notification, and run command if defined.
        """
        if alarm['sound_file']:
            self.play_sound(alarm['sound_file'])
        if alarm['message']:
            self.show_notification(alarm['message'])
        if alarm['command']:
            self.run_command(alarm['command'])

    def play_sound(self, sound_file):
        """
        Play a sound file when the alarm goes off.
        """
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        print(f"Playing sound: {sound_file}")

    def show_notification(self, message):
        """
        Show a desktop notification.
        """
        notification.notify(
            title="Alarm Clock",
            message=message,
            timeout=10  # Notification will stay for 10 seconds
        )
        print(f"Notification: {message}")

    def run_command(self, command):
        """
        Run a system command when the alarm goes off.
        """
        subprocess.run(command, shell=True)
        print(f"Running command: {command}")

# Example usage
if __name__ == "__main__":
    alarm_clock = LinuxAlarmClock()

    # Set alarms
    alarm_clock.set_alarm(
        alarm_time="15:30",
        sound_file="alarm_sound.mp3",
        message="Time to take a break!",
        command="echo 'Break time!'"
    )

    alarm_clock.set_alarm(
        alarm_time="15:35",
        sound_file="alarm_sound.mp3",
        message="Reminder: Back to work!",
        command="notify-send 'Reminder' 'Back to work!'"
    )

    # Check alarms every minute
    alarm_clock.check_alarms()
