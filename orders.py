from models import Order, User, Product
from schemas import OrderModel, UserOrder
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import session, ENGINE

session = session(bind=ENGINE)


order_router = APIRouter(prefix="/orders")

@order_router.get('/')
async def orders():
    orders = session.query(Order).all()
    context = [
        {
            "id": order.id,
            "user": {
                "id": order.users.id,
                "firs_name": order.users.first_name,
                "last_name": order.users.last_name,
                "username": order.users.username,
                "email": order.users.email,
                "is_staff": order.users.is_staff,
                "is_active": order.users.is_active
            },
            "product_id": order.product.id,
            "name": order.product.name,
            "category": {
                "id": order.product.category.id,
                "name": order.product.category.name
            },
            "status": order.order_status
        }
        for order in orders
    ]
    return jsonable_encoder(context)

# @order_router.post("/create")


@order_router.post('/create')
async def create(order: OrderModel):
    check_order = session.query(Order).filter(Order.id == order.id).first()
    check_user_id = session.query(User).filter(User.id == order.user_id).first()
    check_product_id = session.query(Product).filter(Product.id == order.product_id).first()

    if check_order:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already exis")

    elif check_user_id and check_product_id:
        new_order = Order(
            id=order.id,
            user_id=order.user_id,
            product_id=order.product_id,
            count=order.count,
            order_status=order.order_status
        )
        session.add(new_order)
        session.commit()
        data = {
            "secsess": True,
            "code": 201,
            "msg": "creatad sucsess",
            "data": {
                "id": new_order.id,
                "user": {
                    "id": new_order.id,
                    "user": {
                        "id": new_order.users.id,
                        "firs_name": new_order.users.first_name,
                        "last_name": new_order.users.last_name,
                        "username": new_order.users.username,
                        "email": new_order.users.email,
                        "is_staff": new_order.users.is_staff,
                        "is_active": new_order.users.is_active
                    },
                    "product_id": new_order.product.id,
                    "name": new_order.product.name,
                    "price": new_order.product.price,
                    "category": {
                        "id": new_order.product.category.id,
                        "name": new_order.product.category.name,
                    }
                },
            "count": new_order.count,
            "status": new_order.order_status,
            },
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id or product_id allr exis")


@order_router.get("/{id}")
async def get_order_id(id: int):
    check_order = session.query(Order).filter(Order.id == id).first()
    if check_order:
        data = {
            "secsess": True,
            "code": 201,
            "msg": "creatad sucsess",
            "data": {
                "id": check_order.id,
                "user": {
                    "id": check_order.id,
                    "user": {
                        "id": check_order.users.id,
                        "firs_name": check_order.users.first_name,
                        "last_name": check_order.users.last_name,
                        "username": check_order.users.username,
                        "email": check_order.users.email,
                        "is_staff": check_order.users.is_staff,
                        "is_active": check_order.users.is_active
                    },
                    "product_id": check_order.product.id,
                    "name": check_order.product.name,
                    "price": check_order.product.price,
                    "category": {
                        "id": check_order.product.category.id,
                        "name": check_order.product.category.name,
                    }
                },
                "count": check_order.count,
                "status": check_order.order_status,
                "total":check_order.product.price * check_order.count
                "total_balance_promo_cod":check_order.product.price * check_order.count
            },
        }
        promo_cod = "uzum"
        if promo_cod == "uzum":
            data['data']['total_balance_promo_cod'] *= 0.9
            return jsonable_encoder(data)
        else:
            return jsonable_encoder(data)




    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bunday order mavjud emas")


@order_router.post("/user/order")
async def get_user_orders(user_order: UserOrder):
    check_user = session.query(User).filter(User.username == user_order.username).first()
    if check_user:
        check_order = session.query(Order).filter(Order.user.username == user_order.username).first()
        if check_order:
            data = {
                "secsess": True,
                "code": 201,
                "msg": "creatad sucsess",
                "data": {
                    "id": check_order.id,
                    "user": {
                        "id": check_order.id,
                        "user": {
                            "id": check_order.users.id,
                            "firs_name": check_order.users.first_name,
                            "last_name": check_order.users.last_name,
                            "username": check_order.users.username,
                            "email": check_order.users.email,
                            "is_staff": check_order.users.is_staff,
                            "is_active": check_order.users.is_active
                        },
                        "product_id": check_order.product.id,
                        "name": check_order.product.name,
                        "price": check_order.product.price,
                        "category": {
                            "id": check_order.product.category.id,
                            "name": check_order.product.category.name,
                        }
                    },
                    "count": check_order.count,
                    "status": check_order.order_status,
                },
            }
            return jsonable_encoder(data)











