//IMPORT EXTERNAL COMPONENTS================================================
import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Menu, Icon, Label } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const itemClass = css({
    "&&&&:hover": {
        backgroundColor: "deepskyblue"
    }
})

const iconClass = css({
    "&&&&&": {
        marginRight: "0"
    }
})

const labelClass = css({
    "&&&&&": {
        marginLeft: "0"
    }
})

//COMPONENT=================================================================
function CartItem() {
    const { productsType } = useContext(CartContext)

    return (
        <Menu.Item
            as={Link}
            to="/cart"
            className={itemClass}
        >
            <Icon name="shopping cart" size="big" className={iconClass}/>
            <Label color="orange" size="mini" circular className={labelClass}>{productsType}</Label>
        </Menu.Item>
    )
}

//EXPORT COMPONENT==========================================================
export default CartItem;