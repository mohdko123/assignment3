
import pickle
import os
DISCOUNTS = True

def pickle_object(obj):
    '''
    This method will take the object and saves it into the corresponding file of pickle as a tuple.
    :param obj:
    :return:
    '''
    file_mapping = {
        "Event": "events.pkl",
        "Service": "services.pkl",
        "Order": "orders.pkl",
        "Visitor": "visitors.pkl"
    }

    obj_type = type(obj).__name__
    if obj_type not in file_mapping:
        raise ValueError(f"Unsupported object type: {obj_type}")

    file_name = file_mapping[obj_type]

    obj_data = None
    if hasattr(obj, "__dict__"):
        obj_data = obj.__dict__
    else:
        raise ValueError(f"The object of type {obj_type} does not have accessible attributes.")

    if os.path.exists(file_name):
        with open(file_name, "rb") as file:
            existing_data = pickle.load(file)
    else:
        existing_data = []

    existing_data.append(obj_data)

    with open(file_name, "wb") as file:
        pickle.dump(existing_data, file)

    print(f"{obj_type} object has been saved to {file_name}.")


class Event:
    def __init__(self, name, date, description):
        self.__name = name
        self.__date = date
        self.__description = description

        pickle_object(self)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description


    def __str__(self):
        return f"Event(name={self.__name}, date={self.__date}, description={self.__description})"


class Service:
    def __init__(self, name, cost):
        self.__name = name
        self.__cost = cost

        pickle_object(self)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_cost(self):
        return self.__cost

    def set_cost(self, cost):
        self.__cost = cost

    def __str__(self):
        return f"Service(name={self.__name}, cost={self.__cost})"


class ThemePark:
    def __init__(self, name, location):
        self.__name = name
        self.__location = location
        self.__events = []
        self.__services = []
        self.__orders = []
        self.__visitors = []

        t1 = SingleDayPass(1, 275)
        t2 = TwoDayPass(2, 480)
        t3 = AnnualMembership(3,1840)
        t4 = ChildTicket(4,185)
        t5 = GroupPass(5,220)
        t6 = VIPExperience(6,550)

        # creating tickets objects and adding into tickets dictionary
        self.tickets = {"Single Day Pass":t1,
                          "Two Day Pass":t2,
                          "Annual Membership":t3,
                          "Child Ticket":t4,
                          "Group Ticket":t5,
                          "VIP Experience":t6}



    def find_visitor_by_id(self,id):
        '''
        THis method will return the visitor object given a valid id
        '''
        for v in self.__visitors:
            if v.get_visitor_id() == id:
                return v

        return False

    def find_order_by_id(self,id):
        '''
        This method will return order object given valid order id
        '''
        for o in self.__orders:
            if o.get_order_id() == id:
                return o

        return False

    def find_orders_by_visitor_id(self,id):
        '''
        THis method will return list of orders for a visitor given his id
        '''
        orders_list = []
        for order in self.__orders:
            if order.get_visitor_id() == id:
                orders_list.append(order)
        return orders_list

    def fetch_purchase_order_history(self,visitor_id):
        '''
        This method will return the purchase history of the visitor
        '''
        history = ""

        visitor = self.find_visitor_by_id(visitor_id)
        if visitor:
            orders = self.find_orders_by_visitor_id(visitor_id)
            print(orders)
            for order in orders:
                history += order.get_details()

            return history
        else:
            return "visitor not found"

    def total_tickets_sold(self):
        '''
        This method will calculate the total number of tickets and return
        :return:
        '''
        num = 0
        for order in self.__orders:
            num += len(order.get_tickets())
        return num

    def total_revenue(self):
        '''
        THis method will calculate total revenue by adding all the bills and return it.
        :return:
        '''
        num = 0
        for order in self.__orders:
            num += order.get_bill()
        return num

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_max_capacity(self):
        return self.__max_capacity

    def set_max_capacity(self, capacity):
        self.__max_capacity = capacity

    def add_event(self, event):
        self.__events.append(event)

    def get_events(self):
        return self.__events

    def add_service(self, service):
        self.__services.append(service)

    def get_services(self):
        return self.__services

    def get_orders(self):
        return self.__orders

    def get_tickets(self):
        return self.tickets

    def add_order(self,order):
        self.__orders.append(order)

    def add_visitor(self,v):
        self.__visitors.append(v)

    def get_visitors(self):
        return self.__visitors


class Ticket:
    def __init__(self, ticket_id, description, validity, price, ticket_type, discount, limitations):
        self.__ticket_id = ticket_id
        self.__description = description
        self.__validity = validity
        self.__price = price
        self.__type = ticket_type
        self.__discount = discount
        self.__limitations = limitations



    def get_ticket_id(self):
        return self.__ticket_id

    def set_ticket_id(self, ticket_id):
        self.__ticket_id = ticket_id

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_validity(self):
        return self.__validity

    def set_validity(self, validity):
        self.__validity = validity

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_type(self):
        return self.__type

    def set_type(self, ticket_type):
        self.__type = ticket_type

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.__discount = discount

    def get_limitations(self):
        return self.__limitations

    def set_limitations(self, limitations):
        self.__limitations = limitations

    def get_details(self):
        return "\nTicket : {}\tPrice : {}\tValidity : {}\tDiscount : {}\n".format(self.get_ticket_id(),self.get_price(),self.get_validity(),self.get_discount())


class SingleDayPass(Ticket):
    def __init__(self, ticket_id, price):
        super().__init__(
            ticket_id,
            description="Access to the park for one day",
            validity=1,
            price=price,
            ticket_type="Single Day Pass",
            discount=0,
            limitations="Valid only on selected date"
        )


class TwoDayPass(Ticket):
    def __init__(self, ticket_id, price,purchase_type=""):
        super().__init__(
            ticket_id,
            description="Access to the park for two consecutive days",
            validity=2,
            price=price,
            ticket_type="Two Day Pass",
            discount=10,
            limitations="Cannot be split over multiple trips"
        )

        self.__price = price
        self.__purchase_type = purchase_type

    def get_price(self):
        '''
        This method will apply the discount if applicable and returns the price of the ticket
        :return:
        '''
        if not DISCOUNTS:
            return self.__price
        else:
            if self.__purchase_type == "online":
                discount = self.__price * 0.20
                return self.__price - discount
            else:
                return self.__price

    def get_purchase_type(self):
        return self.__purchase_type

    def set_purchase_type(self,pt):
        self.__purchase_type = pt


class AnnualMembership(Ticket):
    def __init__(self, ticket_id, price, renewal=False):
        super().__init__(
            ticket_id,
            description="Unlimited access for one year",
            validity=365,
            price=price,
            ticket_type="Annual Membership",
            discount=15,
            limitations="Must be used by the same person"
        )
        self.__price = price
        self.__renewal = renewal

    def get_price(self):
        '''
        This method will apply the discount if applicable and returns the price of the ticket
        :return:
        '''
        if not DISCOUNTS:
            return self.__price
        else:
            if self.__renewal:
                discount = self.__price * 0.15
                return self.__price - discount
            else:
                return self.__price

    def get_renewal(self):
        return self.__renewal

    def set_renewal(self,ren):
        self.__renewal = ren


class ChildTicket(Ticket):
    def __init__(self, ticket_id, price):
        super().__init__(
            ticket_id,
            description="Discounted Ticket for Children",
            validity=1,
            price=price,
            ticket_type="Child Ticket",
            discount=0,
            limitations="Valid only on selected date must be accompanied by an adult."
        )


class GroupPass(Ticket):
    def __init__(self, ticket_id, price, group_size=10):
        super().__init__(
            ticket_id,
            description="Special rate for groups",
            validity=1,
            price=price,
            ticket_type="Group Pass",
            discount=20,
            limitations=f"Valid for groups of up to {group_size} people"
        )
        self.__group_size = group_size
        self.__price = price

    def get_group_size(self):
        return self.__group_size

    def set_group_size(self, group_size):
        self.__group_size = group_size

    def get_price(self):
        '''
        This method will apply the discount if applicable and returns the price of the ticket
        :return:
        '''
        if not DISCOUNTS:
            return self.__price * self.__group_size
        else:
            if self.__group_size < 20:
                return self.__group_size * self.__price
            else:
                total = self.__group_size * self.__price
                discount = total * 0.20
                return total - discount


class VIPExperience(Ticket):
    def __init__(self, ticket_id, price):
        super().__init__(
            ticket_id,
            description="Includes expedited access and reserved seating for shows",
            validity=1,
            price=price,
            ticket_type="VIP Experience",
            discount=0,
            limitations="Limited Availability Must be purchased in advance."
        )


class Visitor:
    def __init__(self, visitor_id, name, contact_info):
        self.__visitor_id = visitor_id
        self.__name = name
        self.__contact_info = contact_info
        self.__tickets = []

        pickle_object(self)

    def get_visitor_id(self):
        return self.__visitor_id

    def set_visitor_id(self, visitor_id):
        self.__visitor_id = visitor_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_contact_info(self):
        return self.__contact_info

    def set_contact_info(self, contact_info):
        self.__contact_info = contact_info

    def add_ticket(self, ticket):
        self.__tickets.append(ticket)

    def get_tickets(self):
        return self.__tickets


class Order:
    def __init__(self, order_id, visitor_id, date, payment_method,tickets=[]):
        self.__order_id = order_id
        self.__tickets = tickets
        self.__visitor_id = visitor_id
        self.__date = date
        self.__payment_method = payment_method

        pickle_object(self)

    def get_bill(self):
        '''
        This method will calculate the total bill from all the ticket prices
        :return:
        '''
        bill = 0
        for i in self.__tickets:
            bill += i.get_price()
        return bill


    def add_ticket(self,t):
        self.__tickets.append(t)

    def get_order_id(self):
        return self.__order_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def get_tickets(self):
        return self.__tickets

    def set_tickets(self, tickets):
        self.__tickets = tickets

    def get_visitor_id(self):
        return self.__visitor_id

    def set_visitor_id(self, visitor_id):
        self.__visitor_id = visitor_id

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_payment_method(self):
        return self.__payment_method

    def set_payment_method(self, payment_method):
        self.__payment_method = payment_method

    def get_details(self):
        msg = "\n*****************\nOrder : {}\nDate : {}\nPayment Method : {}\nTickets : {}\nTotal Bill : {}".format(self.get_order_id(),self.get_date(),self.get_payment_method(),len(self.get_tickets()),self.get_bill())
        for i in self.__tickets:
            msg += i.get_details()
        return msg




import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel

class ThemeParkWindow:
    def __init__(self):

        self.theme_park = ThemePark("Adventure Land Theme Park","UAE")
        v1 = Visitor("1","Saif","143223")
        v2 = Visitor("2", "Ali", "3984593")
        self.theme_park.add_visitor(v1)
        self.theme_park.add_visitor(v2)

        self.__root = tk.Tk()
        self.__root.title("Adventure Land Theme Park")
        self.__root.geometry("1250x600")
        self.__root.configure(bg="lightblue")

        self.__heading_label = tk.Label(
            self.__root,
            text="Welcome to Adventure Land Theme Park",
            font=("Helvetica", 20, "bold"),
            fg="darkblue",
            bg="lightblue",
            pady=10
        )
        self.__heading_label.pack(anchor="n")

        self.__frame = tk.Frame(self.__root, bg="lightblue")
        self.__frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.__form_frame = tk.Frame(self.__frame, bg="lightblue")
        self.__form_frame.pack(side="left", padx=20, pady=20, fill="both")

        self.__add_visitor_button = tk.Button(
            self.__form_frame,
            text="Add Visitor",
            font=("Helvetica", 12),
            command=self.add_visitor
        )
        self.__add_visitor_button.grid(row=0, column=0, padx=5, pady=5)

        self.__visitor_id_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__visitor_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.set_placeholder(self.__visitor_id_entry, "ID")

        self.__visitor_name_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__visitor_name_entry.grid(row=0, column=2, padx=5, pady=5)
        self.set_placeholder(self.__visitor_name_entry, "Name")

        self.__visitor_contact_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__visitor_contact_entry.grid(row=0, column=3, padx=5, pady=5)
        self.set_placeholder(self.__visitor_contact_entry, "Contact")

        self.__add_event_button = tk.Button(
            self.__form_frame,
            text="Add Event",
            font=("Helvetica", 12),
            command=self.add_event
        )
        self.__add_event_button.grid(row=1, column=0, padx=5, pady=5)

        self.__event_name_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__event_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.set_placeholder(self.__event_name_entry, "Event Name")

        self.__event_date_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__event_date_entry.grid(row=1, column=2, padx=5, pady=5)
        self.set_placeholder(self.__event_date_entry, "Event Date")

        self.__event_description_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__event_description_entry.grid(row=1, column=3, padx=5, pady=5)
        self.set_placeholder(self.__event_description_entry, "Event Description")

        self.__add_service_button = tk.Button(
            self.__form_frame,
            text="Add Service",
            font=("Helvetica", 12),
            command=self.add_service
        )
        self.__add_service_button.grid(row=2, column=0, padx=5, pady=5)

        self.__service_name_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__service_name_entry.grid(row=2, column=1, padx=5, pady=5)
        self.set_placeholder(self.__service_name_entry, "Service Name")

        self.__service_cost_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__service_cost_entry.grid(row=2, column=2, padx=5, pady=5)
        self.set_placeholder(self.__service_cost_entry, "Service Cost")

        self.__generate_order_button = tk.Button(
            self.__form_frame,
            text="Generate Order",
            font=("Helvetica", 12),
            command=self.generate_order
        )
        self.__generate_order_button.grid(row=3, column=0, padx=5, pady=5)

        self.__order_id_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__order_id_entry.grid(row=3, column=1, padx=5, pady=5)
        self.set_placeholder(self.__order_id_entry, "Order ID")

        self.__order_visitor_id_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__order_visitor_id_entry.grid(row=3, column=2, padx=5, pady=5)
        self.set_placeholder(self.__order_visitor_id_entry, "Visitor ID")

        self.__order_date_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__order_date_entry.grid(row=3, column=3, padx=5, pady=5)
        self.set_placeholder(self.__order_date_entry, "Order Date")

        self.__payment_method_dropdown = ttk.Combobox(
            self.__form_frame,
            values=["Credit Card", "Digital Wallet"],
            font=("Helvetica", 12),
            state="readonly"
        )
        self.__payment_method_dropdown.set("Payment Method")
        self.__payment_method_dropdown.grid(row=4, column=3, padx=5, pady=5)


        self.__add_ticket_button = tk.Button(
            self.__form_frame,
            text="Add Ticket",
            font=("Helvetica", 12),
            command=self.add_ticket
        )
        self.__add_ticket_button.grid(row=5, column=0, padx=5, pady=5)

        self.__ticket_order_id_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__ticket_order_id_entry.grid(row=5, column=1, padx=5, pady=5)
        self.set_placeholder(self.__ticket_order_id_entry, "Order ID")

        self.__ticket_dropdown = ttk.Combobox(
            self.__form_frame,
            values=["Single Day Pass","Two Day Pass","Annual Membership","Child Ticket","Group Ticket","VIP Experience"],
            font=("Helvetica", 12),
            state="readonly"
        )
        self.__ticket_dropdown.set("Select Ticket")
        self.__ticket_dropdown.grid(row=5, column=2, padx=5, pady=5)

        self.__purchase_order_history = tk.Button(
            self.__form_frame,
            text="Order History",
            font=("Helvetica", 12),
            command=self.order_history
        )
        self.__purchase_order_history.grid(row=6, column=0, padx=5, pady=5)

        self.__order_history_visitor_id_entry = tk.Entry(self.__form_frame, font=("Helvetica", 12), fg="gray")
        self.__order_history_visitor_id_entry.grid(row=6, column=1, padx=5, pady=5)
        self.set_placeholder(self.__order_history_visitor_id_entry, "Visitor ID")

        self.__view_tickets_button = tk.Button(
            self.__form_frame,
            text="View Tickets",
            font=("Helvetica", 12),
            command=self.view_tickets
        )
        self.__view_tickets_button.grid(row=7, column=0, padx=5, pady=50)

        self.__view_events_button = tk.Button(
            self.__form_frame,
            text="View Events",
            font=("Helvetica", 12),
            command=self.view_events
        )
        self.__view_events_button.grid(row=7, column=1, padx=5, pady=5)

        self.__view_services_button = tk.Button(
            self.__form_frame,
            text="View Services",
            font=("Helvetica", 12),
            command=self.view_services
        )
        self.__view_services_button.grid(row=7, column=2, padx=5, pady=5)

        self.__view_visitors_button = tk.Button(
            self.__form_frame,
            text="View Visitors",
            font=("Helvetica", 12),
            command=self.view_visitors
        )
        self.__view_visitors_button.grid(row=7, column=3, padx=5, pady=5)

        self.__admin_button = tk.Button(
            self.__form_frame,
            text="Admin Dashboard",
            font=("Helvetica", 12),
            command=self.open_admin_dashboard
        )
        self.__admin_button.grid(row=8, column=0, padx=5, pady=10)

        self.__output_label = tk.Label(
            self.__frame,
            text="Output",
            font=("Helvetica", 16),
            fg="black",
            bg="lightblue"
        )
        self.__output_label.pack(anchor="ne", padx=150)

        self.__output_box = tk.Text(
            self.__frame,
            wrap="word",
            font=("Helvetica", 14),
            height=20,
            width=30,
            state="disabled"
        )
        self.__output_box.pack(side="right", padx=10)


    def add_ticket(self):
        '''
        This method will get the data from the fields and validate it
        if validated it will create a ticket int he system
        :return:
        '''
        order_id = self.__ticket_order_id_entry.get().strip()
        ticket_type = self.__ticket_dropdown.get().strip()

        if order_id != "" and order_id != "Order ID" and ticket_type != "Select Ticket":

            order = self.theme_park.find_order_by_id(order_id)
            ticket = self.theme_park.tickets[ticket_type]

            if order and ticket:

                order.add_ticket(ticket)

                self.__output_box.config(state="normal")
                self.__output_box.insert("end", "Ticket added into order successfully\n")
                self.__output_box.config(state="disabled")
            else:
                self.__output_box.config(state="normal")
                self.__output_box.insert("end", "Operation Unsuccessful\n")
                self.__output_box.config(state="disabled")
        else:
            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Operation Unsuccessful\n")
            self.__output_box.config(state="disabled")

    def add_visitor(self):
        '''
        This method will get the data from the GUI and validates it. after validation it will
        create a visitor in the system.
        :return:
        '''
        id = self.__visitor_id_entry.get().strip()
        name = self.__visitor_name_entry.get().strip()
        contact = self.__visitor_contact_entry.get().strip()

        if id != "" and name != "" and contact != "" and id != "ID" and name != "Name" and contact != "Contact":

            visitor = Visitor(id,name,contact)
            self.theme_park.add_visitor(visitor)

            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Visitor added successfully\n")
            self.__output_box.config(state="disabled")

            self.__visitor_id_entry.delete(0, "end")
            self.__visitor_id_entry.insert(0, "ID")
            self.__visitor_id_entry.config(fg="gray")

            self.__visitor_name_entry.delete(0, "end")
            self.__visitor_name_entry.insert(0, "Name")
            self.__visitor_name_entry.config(fg="gray")

            self.__visitor_contact_entry.delete(0, "end")
            self.__visitor_contact_entry.insert(0, "Contact")
            self.__visitor_contact_entry.config(fg="gray")

        else:
            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Operation Unsuccessful\n")
            self.__output_box.config(state="disabled")


    def add_event(self):
        '''
        This method will get the data from the GUI and after validating the vata it will
        add a new event into the system
        :return:
        '''
        name = self.__event_name_entry.get().strip()
        date = self.__event_date_entry.get().strip()
        description = self.__event_description_entry.get().strip()

        if name != "" and date != "" and description != "" and name != "Event Name" and date != "Event Date" and description != "Event Description":

            event = Event(name,date,description)
            self.theme_park.add_event(event)

            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Event added successfully\n")
            self.__output_box.config(state="disabled")

            self.__event_name_entry.delete(0, "end")
            self.__event_name_entry.insert(0, "Event Name")
            self.__event_name_entry.config(fg="gray")

            self.__event_date_entry.delete(0, "end")
            self.__event_date_entry.insert(0, "Event Date")
            self.__event_date_entry.config(fg="gray")

            self.__event_description_entry.delete(0, "end")
            self.__event_description_entry.insert(0, "Event Description")
            self.__event_description_entry.config(fg="gray")

        else:
            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Operation Unsuccessful\n")
            self.__output_box.config(state="disabled")

    def add_service(self):
        name = self.__service_name_entry.get().strip()
        cost = self.__service_cost_entry.get().strip()

        if name != "" and cost != "" and name != "Service Name" and cost != "Service Cost":

            service = Service(name,cost)
            self.theme_park.add_service(service)

            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Service added successfully\n")
            self.__output_box.config(state="disabled")

            self.__service_name_entry.delete(0, "end")
            self.__service_name_entry.insert(0, "Service Name")
            self.__service_name_entry.config(fg="gray")

            self.__service_cost_entry.delete(0, "end")
            self.__service_cost_entry.insert(0, "Service Cost")
            self.__service_cost_entry.config(fg="gray")

        else:
            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Operation Unsuccessful\n")
            self.__output_box.config(state="disabled")

    def generate_order(self):

        '''
        This method will generate the order into system for a visitor

        '''
        order_id = self.__order_id_entry.get().strip()
        visitor_id = self.__order_visitor_id_entry.get().strip()
        date = self.__order_date_entry.get().strip()
        payment_method = self.__payment_method_dropdown.get().strip()

        if order_id != "" and visitor_id != "" and date != "" and order_id != "Order ID" and visitor_id != "Visitor ID" and date != "Date" and payment_method != "Payment Method":

            order = Order(order_id,visitor_id,date,payment_method)
            self.theme_park.add_order(order)

            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Order generated successfully\n")
            self.__output_box.config(state="disabled")

            # Reset fields to placeholders
            self.__order_id_entry.delete(0, "end")
            self.__order_id_entry.insert(0, "Order ID")
            self.__order_id_entry.config(fg="gray")

            self.__order_visitor_id_entry.delete(0, "end")
            self.__order_visitor_id_entry.insert(0, "Visitor ID")
            self.__order_visitor_id_entry.config(fg="gray")

            self.__order_date_entry.delete(0, "end")
            self.__order_date_entry.insert(0, "Order Date")
            self.__order_date_entry.config(fg="gray")

            self.__payment_method_dropdown.set("Payment Method")

        else:
            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Operation Unsuccessful\n")
            self.__output_box.config(state="disabled")



    def order_history(self):
        '''
        This method will take the visitor id and displays all the details of the
        order history in the output.
        :return:
        '''
        visitor_id = self.__order_history_visitor_id_entry.get().strip()

        if visitor_id != "" and visitor_id != "Visitor ID":

            history = self.theme_park.fetch_purchase_order_history(visitor_id)

            self.__output_box.config(state="normal")
            self.__output_box.delete("1.0", "end")
            self.__output_box.insert("end", "{}\n".format(history))
            self.__output_box.config(state="disabled")

            self.__order_history_visitor_id_entry.delete(0, "end")
            self.__order_history_visitor_id_entry.insert(0, "Visitor ID")
            self.__order_history_visitor_id_entry.config(fg="gray")
        else:
            self.__output_box.config(state="normal")
            self.__output_box.insert("end", "Operation Unsuccessful\n")
            self.__output_box.config(state="disabled")

    def view_tickets(self):
        '''
        This method displays a list of all the tickets in the system
        :return:
        '''
        tickets = list(self.theme_park.get_tickets().values())
        result = "Tickets in System : {}\n".format(len(tickets))

        for ticket in tickets:
            result += "\n************\nID : {}\nTicket Type : {}\nPrice : {}\nValidity : {}\nDiscount : {}\nDescription : {}\nLimitation : {}".format(ticket.get_ticket_id(),ticket.get_type(),ticket.get_price(),ticket.get_validity(),ticket.get_discount(),ticket.get_description(),ticket.get_limitations())

        self.__output_box.config(state="normal")
        self.__output_box.delete("1.0", "end")
        self.__output_box.insert("end", "{}\n".format(result))
        self.__output_box.config(state="disabled")

    def view_events(self):
        '''
        This method will display the list of all the events in the system
        :return:
        '''
        events = self.theme_park.get_events()
        result = "Events in System : {}\n".format(len(events))

        for event in events:
            result += "\n************\nName : {}\nDate : {}\nDescription : {}\n".format(event.get_name(),event.get_date(),event.get_description())

        self.__output_box.config(state="normal")
        self.__output_box.delete("1.0", "end")
        self.__output_box.insert("end", "{}\n".format(result))
        self.__output_box.config(state="disabled")


    def view_services(self):
        '''
        This method will display the list of all the services in the system
        :return:
        '''
        services = self.theme_park.get_services()
        result = "Services in System : {}\n".format(len(services))

        for service in services:
            result += "\n************\nName : {}\nCost : {}\n".format(service.get_name(),service.get_cost())

        self.__output_box.config(state="normal")
        self.__output_box.delete("1.0", "end")
        self.__output_box.insert("end", "{}\n".format(result))
        self.__output_box.config(state="disabled")

    def view_visitors(self):
        '''
        This method will display the list of all the visitors in the system
        :return:
        '''
        visitors = self.theme_park.get_visitors()
        result = "Visitors in System : {}\n".format(len(visitors))

        for visitor in visitors:
            result += "\n************\nID : {}\nName : {}\nContact : {}\n".format(visitor.get_visitor_id(),visitor.get_name(),visitor.get_contact_info())

        self.__output_box.config(state="normal")
        self.__output_box.delete("1.0", "end")
        self.__output_box.insert("end", "{}\n".format(result))
        self.__output_box.config(state="disabled")

    # Set placeholder functionality
    def set_placeholder(self, entry, placeholder_text):
        entry.insert(0, placeholder_text)

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, "end")
                entry.config(fg="black")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(fg="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def open_admin_dashboard(self):
        '''
        THis method will display the admin dashboard window with the following information
        Total number of orders
        Total tickets sold
        Total revenue
        :return:
        '''
        admin_window = Toplevel(self.__form_frame)
        admin_window.title("Admin Dashboard")
        admin_window.geometry("400x300")
        admin_window.resizable(False, False)

        total_orders = len(self.theme_park.get_orders())
        total_tickets = self.theme_park.total_tickets_sold()
        total_revenue = self.theme_park.total_revenue()

        tk.Label(admin_window, text="Admin Dashboard", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(admin_window, text="Total Number of Orders:", font=("Helvetica", 12)).pack(anchor="w", padx=20, pady=5)
        tk.Label(admin_window, text="{}".format(total_orders), font=("Helvetica", 12, "bold"), fg="blue").pack(anchor="w", padx=40)

        tk.Label(admin_window, text="Total Tickets Sold:", font=("Helvetica", 12)).pack(anchor="w", padx=20, pady=5)
        tk.Label(admin_window, text="{}".format(total_tickets), font=("Helvetica", 12, "bold"), fg="blue").pack(anchor="w", padx=40)

        tk.Label(admin_window, text="Total Revenue:", font=("Helvetica", 12)).pack(anchor="w", padx=20, pady=5)
        tk.Label(admin_window, text="{} DHS".format(total_revenue), font=("Helvetica", 12, "bold"), fg="green").pack(anchor="w", padx=40)

        tk.Button(admin_window, text="Close", font=("Helvetica", 12), command=admin_window.destroy).pack(pady=20)

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    window = ThemeParkWindow()
    window.run()
    window.run()



