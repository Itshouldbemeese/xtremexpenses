class Observerable():
    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)


    def unsubscribe(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)


    def send_signal(self, value=None, *args, **kwargs):
        for observer in self.observers:
            observer.receive_signal(self, value, *args, **kwargs)


class Observer():
    def receive_signal(self, observable, value=None, *args, **kwargs):
        pass