from __future__ import division
import Queue
import threading

import serial

import util
import constants


class SerialDriver(object):
  """Maintain a serial connection and buffer."""

  def __init__(self, path, baud, timeout=0, messages_per_second=25):
    """Setup the connection and buffers."""
    self.connection = serial.Serial(path, baud, timeout=timeout)
    self.input_buffer = ''
    self.output_message_queue = Queue.Queue()
    self.messages_per_second = messages_per_second * constants.BAY_CONFIG[
      "time_warp"
    ]
    # Start the message writing thread.
    self.writer_thread = threading.Thread(target=self.write_messages)
    self.writer_thread.daemon = True
    self.writer_thread.start()

  def write_messages(self):
    """Write messages from the queue to the connection.

    Intended to be run in a separate thread.
    """
    while True:
      if not self.output_message_queue.empty():
        message = self.output_message_queue.get()
        self.connection.write('%s\r\n' % message)
      util.warped_sleep(1 / self.messages_per_second)

  def send_message(self, message):
    """Write data to the message queue."""
    self.output_message_queue.put(message)

  def get_messages(self):
    """Read data into the buffer, returning when a newline is encountered."""
    self.input_buffer += self.connection.read(1024)
    messages = self.input_buffer.splitlines(True)
    if messages:
      if '\n' in messages[-1]:
        self.input_buffer = ''
        return [m.strip() for m in messages]
      else:
        self.input_buffer = messages[-1]
        return [m.strip() for m in messages[0:-1]]
    else:
      return []
