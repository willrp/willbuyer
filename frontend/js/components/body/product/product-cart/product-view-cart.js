//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Link } from "react-router-dom";
import { Button, Label } from "semantic-ui-react";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const viewButtonClass = css({
    "&&&&&": {
        cursor: "default"
    },
    "&&&&&>.label": {
        backgroundColor: "white",
        color: "deepskyblue",
        borderColor: "deepskyblue"
    },
    "&&&&&>.button": {
        backgroundColor: "deepskyblue",
        color: "black",
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
    }
})

//COMPONENT=================================================================
function ProductViewCart() {
    function render() {
        return(
            <Button
                as="div"
                className={viewButtonClass}
                fluid
                labelPosition="left"
                size="large"
                
            >
                <Label basic pointing="right" size="huge">
                    Product already in cart
                </Label>
                <Button
                    as={Link}
                    to={`/cart`}
                    icon="shopping cart"
                    labelPosition="left"
                    content="View cart"
                    size="huge"
                    fluid
                />
            </Button>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default ProductViewCart;