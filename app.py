from flask import Flask, request, jsonify
from models import db, Service, CompanyInfo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных
db.init_app(app)


@app.route('/api/services', methods=['GET'])
def get_services():
    """Получить все услуги с возможностью фильтрации"""
    # Фильтрация по категории
    category = request.args.get('category')
    price_max = request.args.get('price_max')

    query = Service.query

    if category:
        query = query.filter_by(category=category)

    if price_max:
        try:
            query = query.filter(Service.price <= int(price_max))
        except ValueError:
            return jsonify({'error': 'price_max должен быть числом'}), 400

    services = query.all()
    return jsonify([service.to_dict() for service in services])


@app.route('/api/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Получить конкретную услугу по ID"""
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Услуга не найдена'}), 404

    return jsonify(service.to_dict())


@app.route('/api/services', methods=['POST'])
def create_service():
    """Создать новую услугу"""
    data = request.get_json()

    # Валидация данных
    errors = []

    if not data.get('name'):
        errors.append('Название услуги обязательно')
    elif len(data.get('name', '')) > 100:
        errors.append('Название слишком длинное (макс 100 символов)')

    if not data.get('description'):
        errors.append('Описание услуги обязательно')

    price = data.get('price')
    if not isinstance(price, int) or price <= 0:
        errors.append('Цена должна быть положительным числом')

    if not data.get('category'):
        errors.append('Категория обязательна')

    if not data.get('completion_time'):
        errors.append('Время выполнения обязательно')

    # Проверка на дубликат названия
    existing_service = Service.query.filter_by(name=data.get('name')).first()
    if existing_service:
        errors.append('Услуга с таким названием уже существует')

    if errors:
        return jsonify({'errors': errors}), 400

    # Создание новой услуги
    service = Service(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        currency=data.get('currency', 'RUB'),
        category=data['category'],
        completion_time=data['completion_time']
    )

    db.session.add(service)
    db.session.commit()

    return jsonify(service.to_dict()), 201


@app.route('/api/about', methods=['GET'])
def get_about():
    """Получить информацию о компании"""
    info = CompanyInfo.query.first()
    if not info:
        return jsonify({'error': 'Информация о компании не найдена'}), 404

    return jsonify(info.to_dict())


@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Services API работает!'
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы

        # Добавляем тестовые данные, если их нет
        if not Service.query.first():
            test_services = [
                Service(
                    name="Корпоративный AI-ассистент",
                    description="Умный помощник для автоматизации клиентской поддержки",
                    price=50000,
                    category="customer_support",
                    completion_time="14-21 день"
                ),
                Service(
                    name="Анализ данных с помощью AI",
                    description="Помощник который будет анализировать ваши данные",
                    price=100000,
                    category="data_analysis",
                    completion_time="14-21 день"
                )
            ]

            for service in test_services:
                db.session.add(service)

        # Добавляем информацию о компании
        if not CompanyInfo.query.first():
            company_info = CompanyInfo(
                company_name="AI Solutions",
                description="Мы создаем AI-агентов для бизнеса",
                founded_year=2024,
                team_size=5,
                email="info@ai-solutions.ru",
                phone="+7 (999) 123-45-67"
            )
            db.session.add(company_info)

        db.session.commit()

    app.run(debug=True)
