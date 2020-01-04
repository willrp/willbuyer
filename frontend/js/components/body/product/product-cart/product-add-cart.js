//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState, useContext } from "react";
import { Form } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const addButtonClass = css({
    "&&&&&&&>.button": {
        height: "100%"
    }
})

//COMPONENT=================================================================
function ProductAddCart({ productid }) {
    const [quantity, setQuantity] = useState(1);
    const { updatingCart, updateCartItem } = useContext(CartContext);

    function onChangeQuantity(e, { value }) {
        setQuantity(value);
    }

    function onSubmit() {
        if(!updatingCart){
            updateCartItem(productid, quantity);
        }
    }

    function render() {
        const options = [...Array(30).keys()].map(
            (item) => {
                return {
                    key: item + 1,
                    text: item + 1,
                    value: item + 1
                }
            }
        )

        return(
            <Form unstackable onSubmit={onSubmit}>
                <Form.Group>
                    <Form.Select
                        width={4}
                        compact
                        label="Quantity"
                        options={options}
                        value={quantity}
                        onChange={onChangeQuantity}
                    />
                    <Form.Button
                        className={addButtonClass}
                        color="green"
                        width={12}
                        fluid
                        size="huge"
                        labelPosition="left"
                        icon="shopping cart"
                        content="Add to cart"
                        loading={updatingCart}
                    />
                </Form.Group>
            </Form>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default ProductAddCart;