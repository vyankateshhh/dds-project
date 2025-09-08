from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

# ---------- Models ----------
@dataclass
class Message:
    sender: str
    content: str
    ts: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None  # optional unique id if you want

    def __repr__(self):
        # compact representation for logs
        t = self.ts.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{t} UTC] {self.sender}: {self.content}"

# ---------- Core Manager ----------
class ChatHistoryManager:
    def __init__(self):
        # Incoming messages (FIFO)
        self.incoming_queue: deque[Message] = deque()
        # Sent history & undo/redo stacks (LIFO)
        self.sent_history: List[Message] = []     # full history of sent messages (for reference/export)
        self._undo_stack: List[Message] = []      # actions we can undo (last sent)
        self._redo_stack: List[Message] = []      # actions we can redo (last undone)
        self._next_id = 1

    # ---- Incoming (Queue) ----
    def enqueue_incoming(self, sender: str, content: str) -> Message:
        msg = Message(sender=sender, content=content, id=self._allocate_id())
        self.incoming_queue.append(msg)
        return msg

    def dequeue_incoming(self) -> Optional[Message]:
        return self.incoming_queue.popleft() if self.incoming_queue else None

    # ---- Sending (with undo/redo) ----
    def send(self, sender: str, content: str) -> Message:
        """
        Sends a message: adds to history and makes it undoable.
        Clears redo stack (standard editor behavior).
        """
        msg = Message(sender=sender, content=content, id=self._allocate_id())
        self.sent_history.append(msg)
        self._undo_stack.append(msg)
        self._redo_stack.clear()
        return msg

    def undo(self) -> Optional[Message]:
        """
        Undo last send: removes it from 'visible' history and moves to redo.
        Returns the undone message (so the UI can show 'message unsent').
        """
        if not self._undo_stack:
            return None
        msg = self._undo_stack.pop()
        self._redo_stack.append(msg)
        # mark as retracted in history, or remove from view.
        # Here we keep in sent_history for audit, but flag retracted:
        self._mark_retracted(msg.id)
        return msg

    def redo(self) -> Optional[Message]:
        """
        Redo last undone send: re-sends the message (restores it).
        """
        if not self._redo_stack:
            return None
        msg = self._redo_stack.pop()
        self._undo_stack.append(msg)
        self._unmark_retracted(msg.id)
        return msg

    # ---- Helpers ----
    def _allocate_id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid

    def _mark_retracted(self, mid: int) -> None:
        for m in self.sent_history:
            if m.id == mid:
                # A simple approach is to append a tag; in a real app, add a boolean flag.
                if not m.content.endswith(" (retracted)"):
                    m.content += " (retracted)"
                return

    def _unmark_retracted(self, mid: int) -> None:
        for m in self.sent_history:
            if m.id == mid and m.content.endswith(" (retracted)"):
                m.content = m.content[: -len(" (retracted)")]
                return

    # ---- Inspection / Export ----
    def peek_incoming(self) -> Optional[Message]:
        return self.incoming_queue[0] if self.incoming_queue else None

    def list_incoming(self) -> List[Message]:
        return list(self.incoming_queue)

    def list_sent(self, include_retracted=True) -> List[Message]:
        if include_retracted:
            return list(self.sent_history)
        return [m for m in self.sent_history if not m.content.endswith(" (retracted)")]

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)


# ---------- Demo ----------
if __name__ == "__main__":
    mgr = ChatHistoryManager()

    # Incoming messages (Queue)
    mgr.enqueue_incoming("Alice", "Hey, are you free?")
    mgr.enqueue_incoming("Bob", "Check this link!")
    print("Incoming queue:", mgr.list_incoming())

    # Handle/consume one incoming
    handled = mgr.dequeue_incoming()
    print("Dequeued incoming:", handled)
    print("Incoming queue after dequeue:", mgr.list_incoming())

    # Send messages (Stack for undo/redo)
    m1 = mgr.send("Me", "Hello Alice!")
    m2 = mgr.send("Me", "Yes, I’m free now.")
    print("\nSent history:", mgr.list_sent())

    # Undo last sent
    u = mgr.undo()
    print("\nUndo:", u)
    print("Sent (with retracted marked):", mgr.list_sent())

    # Redo the undone send
    r = mgr.redo()
    print("\nRedo:", r)
    print("Sent after redo:", mgr.list_sent(include_retracted=False))
