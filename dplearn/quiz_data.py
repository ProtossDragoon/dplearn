DESIGN_PATTERNS = [
    {
        'name': 'Singleton',
        'description': '클래스의 인스턴스가 오직 하나만 생성되고, 그 인스턴스에 대한 전역 접근점을 제공하는 패턴',
    },
    {
        'name': 'Factory Method',
        'description': '객체 생성을 서브클래스에 위임하여 결합도를 낮추는 패턴',
    },
    {
        'name': 'Abstract Factory',
        'description': '관련 객체들의 집합을 생성하기 위한 인터페이스를 제공하는 패턴',
    },
    {
        'name': 'Builder',
        'description': '복잡한 객체의 생성 과정과 표현 방법을 분리하여 다양한 구성의 인스턴스를 만드는 패턴',
    },
    {
        'name': 'Prototype',
        'description': '기존 객체를 복제하여 새 객체를 생성하는 패턴',
    },
    {
        'name': 'Adapter',
        'description': '인터페이스를 다른 인터페이스로 변환하여 호환성 문제를 해결하는 패턴',
    },
    {
        'name': 'Bridge',
        'description': '추상화와 구현을 분리하여 독립적으로 변경할 수 있게 하는 패턴',
    },
    {
        'name': 'Composite',
        'description': '객체들을 트리 구조로 구성하여 부분-전체 계층을 표현하는 패턴',
    },
    {
        'name': 'Decorator',
        'description': '객체에 동적으로 새로운 책임을 추가하는 패턴',
    },
    {
        'name': 'Facade',
        'description': '복잡한 서브시스템에 대한 간단한 인터페이스를 제공하는 패턴',
    },
    {
        'name': 'Flyweight',
        'description': '많은 수의 유사한 객체를 효율적으로 관리하기 위한 패턴',
    },
    {
        'name': 'Proxy',
        'description': '다른 객체에 대한 접근을 제어하는 대리 객체를 제공하는 패턴',
    },
    {
        'name': 'Chain of Responsibility',
        'description': '요청을 처리할 수 있는 객체가 여러 개 있을 때, 그 객체들을 사슬처럼 연결하는 패턴',
    },
    {
        'name': 'Command',
        'description': '요청을 객체로 캡슐화하여 서로 다른 요청을 매개변수화하고 저장하는 패턴',
    },
    {
        'name': 'Iterator',
        'description': '컬렉션의 내부 구조를 노출하지 않고 순차적으로 접근하는 방법을 제공하는 패턴',
    },
    {
        'name': 'Mediator',
        'description': '객체 간의 상호작용을 중재자를 통해 간접적으로 수행하는 패턴',
    },
    {
        'name': 'Memento',
        'description': '객체의 내부 상태를 저장하고 나중에 복원할 수 있게 하는 패턴',
    },
    {
        'name': 'Observer',
        'description': '객체 간의 일대다 의존 관계를 정의하여 상태 변경 시 자동 통지하는 패턴',
    },
    {
        'name': 'State',
        'description': '객체의 내부 상태에 따라 행동을 변경하는 패턴',
    },
    {
        'name': 'Strategy',
        'description': '알고리즘을 정의하고 캡슐화하여 교체 가능하게 만드는 패턴',
    },
    {
        'name': 'Template Method',
        'description': '알고리즘의 구조를 정의하고 일부 단계를 서브클래스에서 구현하는 패턴',
    },
    {
        'name': 'Visitor',
        'description': '객체 구조를 방문하여 각 요소에 대해 연산을 수행하는 패턴',
    },
]

QUIZ_QUESTIONS = [
    {
        'pattern_id': 1,  # Singleton
        'code_example': """
# 시나리오: 애플리케이션 전체에서 데이터베이스 연결을 하나만 유지해야 합니다.
# 여러 연결을 생성하면 리소스 낭비와 데이터 불일치가 발생할 수 있습니다.

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("새로운 데이터베이스 연결을 생성합니다.")
            cls._instance = super().__new__(cls)
            # 실제 연결 설정 작업이 여기서 이루어짐
            cls._instance.connect()
        return cls._instance
    
    def connect(self):
        print("데이터베이스에 연결 중...")
        # 실제 연결 로직
        
    def execute_query(self, query):
        print(f"쿼리 실행: {query}")
        # 쿼리 실행 로직

# 클라이언트 코드
print("첫 번째 연결 요청")
conn1 = DatabaseConnection()
conn1.execute_query("SELECT * FROM users")

print("\\n두 번째 연결 요청")
conn2 = DatabaseConnection()
conn2.execute_query("SELECT * FROM products")

print(f"\\n두 연결이 동일한지 확인: {conn1 is conn2}")  # True 출력
""",
    },
    {
        'pattern_id': 2,  # Factory Method
        'code_example': """
# 시나리오: 다양한 운송 방법(육로, 해상)을 처리하는 물류 관리 시스템을 개발해야 합니다.
# 시스템은 운송 방법에 관계없이 일관된 인터페이스를 제공해야 합니다.

from abc import ABC, abstractmethod

class LogisticsManager(ABC):
    def plan_delivery(self, source, destination):
        # 배송 계획 템플릿 메서드
        transport = self.create_transport()
        print(f"{source}에서 {destination}까지 배송 계획 수립 중...")
        return f"운송 수단: {transport.deliver()}"
    
    @abstractmethod
    def create_transport(self):
        pass

class RoadLogistics(LogisticsManager):
    def create_transport(self):
        return Truck()

class SeaLogistics(LogisticsManager):
    def create_transport(self):
        return Ship()

class Transport(ABC):
    @abstractmethod
    def deliver(self):
        pass

class Truck(Transport):
    def deliver(self):
        return "트럭으로 화물 배송"

class Ship(Transport):
    def deliver(self):
        return "선박으로 화물 배송"

# 클라이언트 코드
def delivery_service(logistics, source, destination):
    return logistics.plan_delivery(source, destination)

# 육로 배송
road_logistics = RoadLogistics()
print(delivery_service(road_logistics, "서울", "부산"))

# 해상 배송
sea_logistics = SeaLogistics()
print(delivery_service(sea_logistics, "부산", "제주"))
""",
    },
    {
        'pattern_id': 3,  # Abstract Factory
        'code_example': """
# 시나리오: 다양한 스타일(모던, 빈티지)의 가구(의자, 테이블)를 생산하는 
# 가구 제조 시스템을 개발해야 합니다. 스타일 간의 일관성을 유지해야 합니다.

from abc import ABC, abstractmethod

class FurnitureFactory(ABC):
    @abstractmethod
    def create_chair(self):
        pass
    
    @abstractmethod
    def create_table(self):
        pass

class ModernFurnitureFactory(FurnitureFactory):
    def create_chair(self):
        return ModernChair()
    
    def create_table(self):
        return ModernTable()

class VintageFurnitureFactory(FurnitureFactory):
    def create_chair(self):
        return VintageChair()
    
    def create_table(self):
        return VintageTable()

class Chair(ABC):
    @abstractmethod
    def sit_on(self):
        pass

class Table(ABC):
    @abstractmethod
    def place_on(self):
        pass

class ModernChair(Chair):
    def sit_on(self):
        return "모던 스타일 의자에 앉음"

class VintageChair(Chair):
    def sit_on(self):
        return "빈티지 스타일 의자에 앉음"

class ModernTable(Table):
    def place_on(self):
        return "모던 스타일 테이블에 물건을 놓음"

class VintageTable(Table):
    def place_on(self):
        return "빈티지 스타일 테이블에 물건을 놓음"

# 클라이언트 코드
def create_furniture_set(factory):
    chair = factory.create_chair()
    table = factory.create_table()
    
    return f"{chair.sit_on()}, {table.place_on()}"

# 모던 스타일 가구 세트 생성
modern_factory = ModernFurnitureFactory()
print(create_furniture_set(modern_factory))

# 빈티지 스타일 가구 세트 생성
vintage_factory = VintageFurnitureFactory()
print(create_furniture_set(vintage_factory))
""",
    },
    {
        'pattern_id': 4,  # Builder
        'code_example': """
# 시나리오: 다양한 옵션(엔진 종류, 내비게이션, 선루프 등)이 있는 
# 자동차 구성 시스템을 개발해야 합니다. 복잡한 객체 생성 과정을 단순화해야 합니다.

class Car:
    def __init__(self):
        self.seats = None
        self.engine = None
        self.navigation = None
        self.sunroof = None
    
    def __str__(self):
        features = []
        if self.seats: features.append(f"좌석: {self.seats}개")
        if self.engine: features.append(f"엔진: {self.engine}")
        if self.navigation: features.append("내비게이션: 장착")
        if self.sunroof: features.append("선루프: 장착")
        
        return "자동차 구성: " + ", ".join(features)

class CarConfigurator:
    def __init__(self):
        self.car = Car()
    
    def set_seats(self, count):
        self.car.seats = count
        return self
    
    def set_engine(self, engine_type):
        self.car.engine = engine_type
        return self
    
    def set_navigation(self, has_navigation):
        self.car.navigation = has_navigation
        return self
    
    def set_sunroof(self, has_sunroof):
        self.car.sunroof = has_sunroof
        return self
    
    def build(self):
        return self.car

# 클라이언트 코드
# 스포츠카 구성
sports_car = CarConfigurator()\
    .set_seats(2)\
    .set_engine("V8")\
    .set_navigation(True)\
    .set_sunroof(True)\
    .build()

print(sports_car)

# 패밀리카 구성
family_car = CarConfigurator()\
    .set_seats(5)\
    .set_engine("V6")\
    .set_navigation(True)\
    .set_sunroof(False)\
    .build()

print(family_car)
""",
    },
    {
        'pattern_id': 5,  # Prototype
        'code_example': """
# 시나리오: 3D 모델링 소프트웨어에서 복잡한 도형 객체를 복제하여 
# 새로운 객체를 생성해야 합니다. 객체 생성 비용을 줄이고 싶습니다.

import copy

class Shape:
    def clone(self):
        return copy.deepcopy(self)

class Rectangle(Shape):
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
    
    def __str__(self):
        return f"{self.color} 직사각형 (가로: {self.width}, 세로: {self.height})"

class Circle(Shape):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
    
    def __str__(self):
        return f"{self.color} 원 (반지름: {self.radius})"

# 클라이언트 코드
# 원본 객체 생성
original_rectangle = Rectangle(10, 5, "빨간색")
print("원본:", original_rectangle)

# 객체 복제 및 수정
cloned_rectangle = original_rectangle.clone()
cloned_rectangle.color = "파란색"
print("복제본:", cloned_rectangle)

original_circle = Circle(5, "노란색")
print("원본:", original_circle)

cloned_circle = original_circle.clone()
cloned_circle.radius = 10
print("복제본:", cloned_circle)

# 원본과 복제본이 다른 객체인지 확인
print(f"원본과 복제본이 다른 객체인가?: {original_rectangle is not cloned_rectangle}")
""",
    },
    {
        'pattern_id': 6,  # Adapter
        'code_example': """
# 시나리오: 레거시 결제 시스템을 새로운 온라인 상점에 통합해야 합니다.
# 두 시스템의 인터페이스가 호환되지 않아 중간 계층이 필요합니다.

class NewPaymentSystem:
    def process_payment(self, amount, currency):
        return f"{amount} {currency}로 결제 처리됨"

class LegacyPaymentProcessor:
    def make_payment(self, price_cents, currency_code):
        return f"{price_cents/100} {currency_code}로 레거시 시스템에서 결제 처리됨"

class PaymentAdapter(NewPaymentSystem):
    def __init__(self, legacy_processor):
        self.legacy_processor = legacy_processor
    
    def process_payment(self, amount, currency):
        # 새 시스템 인터페이스를 레거시 시스템 인터페이스로 변환
        price_cents = int(amount * 100)
        currency_code = self.convert_currency_code(currency)
        return self.legacy_processor.make_payment(price_cents, currency_code)
    
    def convert_currency_code(self, currency):
        # 통화 코드 변환 로직
        currency_map = {"달러": "USD", "유로": "EUR", "원": "KRW"}
        return currency_map.get(currency, currency)

# 클라이언트 코드
def shop_payment_process(payment_processor, amount, currency):
    print(f"상점에서 {amount} {currency} 결제 요청")
    return payment_processor.process_payment(amount, currency)

# 새 결제 시스템 사용
new_system = NewPaymentSystem()
print(shop_payment_process(new_system, 100, "달러"))

# 레거시 시스템을 어댑터를 통해 사용
legacy_system = LegacyPaymentProcessor()
adapter = PaymentAdapter(legacy_system)
print(shop_payment_process(adapter, 100, "달러"))
""",
    },
    {
        'pattern_id': 9,  # Decorator
        'code_example': """
# 시나리오: 텍스트 처리 라이브러리에서 다양한 형식(암호화, 압축, 마크다운 등)의 
# 텍스트 변환 기능을 유연하게 조합하여 사용하고 싶습니다.

from abc import ABC, abstractmethod

class TextProcessor(ABC):
    @abstractmethod
    def process(self, text):
        pass

class BasicTextProcessor(TextProcessor):
    def process(self, text):
        return text

class TextProcessorEnhancer(TextProcessor):
    def __init__(self, text_processor):
        self._text_processor = text_processor
    
    @abstractmethod
    def process(self, text):
        pass

class EncryptionEnhancer(TextProcessorEnhancer):
    def process(self, text):
        # 간단한 암호화 로직
        encrypted = self._text_processor.process(text)
        return f"[암호화됨: {encrypted}]"

class CompressionEnhancer(TextProcessorEnhancer):
    def process(self, text):
        # 간단한 압축 로직
        compressed = self._text_processor.process(text)
        return f"[압축됨: {compressed[:3]}...]"

class MarkdownEnhancer(TextProcessorEnhancer):
    def process(self, text):
        # 마크다운 변환 로직
        markdown = self._text_processor.process(text)
        return f"**{markdown}**"

# 클라이언트 코드
text = "안녕하세요, 텍스트 처리 예제입니다."

# 기본 텍스트 처리
basic = BasicTextProcessor()
print("기본:", basic.process(text))

# 마크다운 변환 추가
markdown = MarkdownEnhancer(basic)
print("마크다운:", markdown.process(text))

# 암호화 추가
encrypted = EncryptionEnhancer(basic)
print("암호화:", encrypted.process(text))

# 여러 기능 조합
combined = CompressionEnhancer(EncryptionEnhancer(MarkdownEnhancer(basic)))
print("조합:", combined.process(text))
""",
    },
    {
        'pattern_id': 18,  # Observer
        'code_example': """
# 시나리오: 온라인 쇼핑몰에서 재고가 부족한 상품이 입고될 때 
# 관심 고객들에게 자동으로 알림을 보내야 합니다.

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.in_stock = False
        self._interested_customers = []
    
    def register_interest(self, customer):
        self._interested_customers.append(customer)
        print(f"{customer.name}님이 {self.name} 입고 알림을 신청했습니다.")
    
    def remove_interest(self, customer):
        self._interested_customers.remove(customer)
        print(f"{customer.name}님이 {self.name} 입고 알림을 취소했습니다.")
    
    def notify_all(self):
        for customer in self._interested_customers:
            customer.update(self)
    
    def restock(self):
        print(f"{self.name} 상품이 재입고되었습니다!")
        self.in_stock = True
        self.notify_all()

class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def update(self, product):
        print(f"{self.name}님에게 이메일 발송: {product.name}이(가) 재입고되었습니다! 가격: {product.price}원")

# 클라이언트 코드
# 상품 생성
phone = Product("스마트폰 X", 1200000)

# 고객 생성
customer1 = Customer("김철수", "kim@example.com")
customer2 = Customer("이영희", "lee@example.com")

# 관심 등록
phone.register_interest(customer1)
phone.register_interest(customer2)

# 재입고 발생
phone.restock()

# 한 고객이 관심 취소
phone.remove_interest(customer1)

# 다시 재입고 발생
phone.in_stock = False  # 일시적으로 품절 상태로 설정
phone.restock()  # 재입고 시 이영희에게만 알림
""",
    },
    {
        'pattern_id': 20,  # Strategy
        'code_example': """
# 시나리오: 온라인 결제 시스템에서 다양한 결제 방법(카드, 계좌이체, 가상화폐)을 
# 지원하고 쉽게 추가할 수 있는 유연한 시스템이 필요합니다.

class PaymentProcessor:
    def __init__(self, payment_method):
        self._payment_method = payment_method
    
    def set_payment_method(self, payment_method):
        self._payment_method = payment_method
    
    def process_payment(self, amount):
        return self._payment_method.process(amount)

class PaymentMethod:
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        # 카드 결제 처리 로직
        return f"{amount}원을 신용카드로 결제했습니다."

class BankTransferPayment(PaymentMethod):
    def process(self, amount):
        # 계좌이체 처리 로직
        return f"{amount}원을 계좌이체로 결제했습니다."

class CryptoPayment(PaymentMethod):
    def process(self, amount):
        # 가상화폐 결제 처리 로직
        return f"{amount}원 상당의 가상화폐로 결제했습니다."

# 클라이언트 코드
def checkout(processor, amount):
    print(f"결제 금액: {amount}원")
    return processor.process_payment(amount)

# 신용카드 결제
card_payment = CreditCardPayment()
processor = PaymentProcessor(card_payment)
print(checkout(processor, 50000))

# 계좌이체로 결제 방식 변경
bank_payment = BankTransferPayment()
processor.set_payment_method(bank_payment)
print(checkout(processor, 50000))

# 가상화폐 결제로 변경
crypto_payment = CryptoPayment()
processor.set_payment_method(crypto_payment)
print(checkout(processor, 50000))
""",
    },
    {
        'pattern_id': 21,  # Template Method
        'code_example': """
# 시나리오: 데이터 분석 애플리케이션에서 다양한 데이터 소스(CSV, 데이터베이스, API)에서
# 데이터를 불러와 처리하는 일관된 프로세스를 정의해야 합니다.

from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def process_data(self):
        data = self.extract()
        clean_data = self.transform(data)
        self.load(clean_data)
        self.notify_completion()
    
    @abstractmethod
    def extract(self):
        # 소스에서 데이터 추출
        pass
    
    @abstractmethod
    def transform(self, data):
        # 데이터 변환 및 정제
        pass
    
    @abstractmethod
    def load(self, clean_data):
        # 처리된 데이터 저장
        pass
    
    def notify_completion(self):
        # 처리 완료 알림 (선택적 후크)
        print("데이터 처리가 완료되었습니다.")

class CSVDataProcessor(DataProcessor):
    def extract(self):
        print("CSV 파일에서 데이터 추출 중...")
        return "CSV 데이터"
    
    def transform(self, data):
        print(f"{data} 정제 중...")
        return f"정제된 {data}"
    
    def load(self, clean_data):
        print(f"{clean_data}를 데이터베이스에 저장 중...")

class APIDataProcessor(DataProcessor):
    def extract(self):
        print("API에서 데이터 추출 중...")
        return "API 데이터"
    
    def transform(self, data):
        print(f"{data} 정제 및 형식 변환 중...")
        return f"변환된 {data}"
    
    def load(self, clean_data):
        print(f"{clean_data}를 데이터 웨어하우스에 저장 중...")
    
    # 후크 메서드 재정의
    def notify_completion(self):
        print("API 데이터 처리 완료! 관리자에게 이메일 발송 중...")

# 클라이언트 코드
print("CSV 처리 시작:")
csv_processor = CSVDataProcessor()
csv_processor.process_data()

print("\\nAPI 처리 시작:")
api_processor = APIDataProcessor()
api_processor.process_data()
""",
    },
]
