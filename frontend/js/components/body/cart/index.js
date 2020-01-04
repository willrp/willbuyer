//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useContext } from "react";
import { Header, Message, Icon } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import OrderButton from "./order-button";
import CartInfo from "./cart-info";
import CartItems from "./cart-items";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const headerClass = css({
    "&&&&&": {
        marginTop: "0.5em"
    }
})

//COMPONENT=================================================================
function Cart() {
    const { products, productsType, itemCount, total } = useContext(CartContext);

    function renderEmptyCart() {
        return (
            <Message icon info className={headerClass}>
                <Icon name="shopping cart" />
                <Message.Content>
                    <Message.Header>Information</Message.Header>
                    Your shopping cart is empty.
                </Message.Content>
            </Message>
        )
    }

    function renderCart() {
        return (
            <Fragment>
                <CartInfo {...{productsType, itemCount, total}} />
                <OrderButton />
                <CartItems items={products} />
            </Fragment>
        )
    }

    function render() {
        return (
            <Fragment>
                <Header className={headerClass} as="h1" textAlign="center" dividing>Shopping Cart</Header>
                {(itemCount === 0) ? renderEmptyCart() : renderCart()}
            </Fragment>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default Cart;