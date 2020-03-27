from utils import exp_dist, inverse_method, normal_dist

class My_logic:
    def __init__(self,sellers = 2, techniclas = 3, esp_technicals = 1):
        self.clients_queue = []
        self.rep_queue = []
        self.sellers_queue = []
        for i in range(sellers):
            self.sellers_queue.append((0,i + 1))
        self.techniclas_queue = []
        for i in range(techniclas):
            self.techniclas_queue.append((0,i + 1))
        self.esp_technicals_queue = []
        for i in range(esp_technicals):
            self.esp_technicals_queue.append((0,i + 1))
        self.table = [(2, 0.45), (2, 0.25), (2, 0.1), (2, 0.2)]
        self.time = 0
        self.money = 0
        self.sellers_timeout = False

    def run_simulation(self, total_time):
        next_client = total_time + 1
        while next_client > total_time:
            next_client = exp_dist(1/20)
        self.clients_queue.append((next_client, inverse_method(self.table), 1))
        number_client = 1
        print('cliente numero ' + str(number_client) + ' llega a la hora ' + str(next_client))
        print('requiere servicio numero ' + str(self.clients_queue[-1][1]))
        
        for time in range(total_time):
            if len(self.clients_queue) == 0 or self.clients_queue[0][0] <= time:
                next_client = time + exp_dist(1/20)
                if next_client < total_time and not self.sellers_timeout:
                    number_client += 1
                    print()
                    print('cliente numero ' + str(number_client) + ' llega a la hora ' + str(next_client))
                    self.clients_queue.append((next_client, inverse_method(self.table), number_client))
                    print('requiere servicio numero ' + str(self.clients_queue[-1][1]))
            self.time = time
            self.seller(total_time)
            self.rep_change(total_time)

    def seller(self, total_time):
        for time in range(self.time, total_time):
            if len(self.clients_queue) == 0:
                break
            if self.clients_queue[0][0] <= time:
                if self.sellers_queue[0][0] <= time:
                    actual_seller = self.sellers_queue.pop(0)
                    actual_client = self.clients_queue.pop(0)
                    delay_time = time + normal_dist()
                    if delay_time <= total_time:
                        print('el vendedor ' + str(actual_seller[1]) + ' termino de atender al cliente ' + str(actual_client[2]) + ' al minuto ' + str(delay_time))
                        self.sellers_queue.append((delay_time, actual_seller[1]))
                    else:
                        self.sellers_timeout = True
                        print('No hay tiempo para atender a mas ningun cliente')
                    if actual_client[1] == 4:
                        self.money += 750
                        print('cliente paga por un equipo reparado. Dinero recaudado hasta ahora ' + str(self.money))
                    else:
                        self.rep_queue.append((delay_time, actual_client[1], actual_client[2]))
    
    def rep_change(self, total_time):
        for time in range(self.time, total_time):
            if len(self.rep_queue) == 0:
                break
            if self.rep_queue[0][0] <= time:
                if self.rep_queue[0][1] != 3 and self.techniclas_queue[0][0] <= time:
                    actual_technical = self.techniclas_queue.pop(0)
                    actual_client = self.rep_queue.pop(0)
                    delay_time = time + exp_dist(1/20)
                    if delay_time <= total_time:
                        print('el tecnico ' + str(actual_technical[1]) + ' termino de atender al cliente ' + str(actual_client[2]) + ' al minuto ' + str(delay_time))
                        self.techniclas_queue.append((delay_time, actual_technical[1]))
                    else:
                        self.sellers_timeout = True
                        print('No hay tiempo para atender a mas ningun cliente')
                    if actual_client[1] == 2:
                        self.money += 350
                        print('cliente paga por una reparacion sin garantia. Dinero recaudado hasta ahora ' + str(self.money))
                
                elif self.esp_technicals_queue[0][0] <= time and (self.rep_queue[0][1] == 3 or self.verificando()):
                    actual_esp_technical = self.esp_technicals_queue.pop(0)
                    actual_client = self.rep_queue.pop(0)
                    delay_time = time + exp_dist(1/15)
                    if delay_time <= total_time:
                        print('el tecnico especializado ' + str(actual_esp_technical[1]) + ' termino de atender al cliente ' + str(actual_client[2]) + ' al minuto ' + str(delay_time))
                        self.esp_technicals_queue.append((delay_time, actual_esp_technical[1]))
                    else:
                        self.sellers_timeout = True
                        print('No hay tiempo para atender a mas ningun cliente')
                    if actual_client[1] == 2:
                        self.money += 350
                        print('client paga por una reparacion sin garantia. Dinero recaudado hasta ahora ' + str(self.money))
                    if actual_client[1] == 3:
                        self.money += 500
                        print('client paga por un cambio de equipo. Dinero recaudado hasta ahora ' + str(self.money))

    def verificando(self):
        for client in self.clients_queue:
            if client[1] == 3:
                return False
        for client in self.rep_queue:
            if client[1] == 3:
                return False
        return True

sim = My_logic()
sim.run_simulation(480)







