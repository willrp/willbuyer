//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState, useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import { Segment, Image, Label, Icon, Header, Select } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const imgClass = css({
    "&&&&&": {
        padding: "0.25em",
        minWidth: "107px",
        maxWidth: "107px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
    "&&&&&>img": {
        minWidth: "100px",
        maxWidth: "100px",
        minHeight: "128px",
        maxHeight: "128px",
    }
})

const infoClass = css({
    "&&&&&": {
        padding: "0.5em"
    },
    "&&&&& .headerdiv": {
        paddingRight: "2em"
    },
    "&&&&& p": {
        margin: "0.25em"
    },
    "&&&&& .corner:hover, &&&&& .corner>i:hover": {
        cursor: "pointer"
    }
})

const retailPriceClass = css({
    "&&&&&": {
        textDecoration: "line-through",
        opacity: 0.4
    }
})

const outletPriceClass = css({
    "&&&&&": {
        color: "red",
        fontWeight: "bold"
    }
})

//COMPONENT=================================================================
function OrderItem({ id, name, image, price, discount, amount }) {
    function render() {
        return (
            <Segment.Group horizontal>
                <Segment 
                    className={imgClass}
                    as={Link}
                    to={`/product/${id}`}
                >
                    <Image src={image.replace("wid=500", "wid=120")} alt=" " />
                </Segment>
                <Segment className={infoClass}>
                    <div className="headerdiv">
                        <Header size="small" as={Link} to={`/product/${id}`}>{name}</Header>
                    </div>
                    <p>
                        <span className={retailPriceClass}>{price.symbol}{price.retail.toFixed(2)}</span>
                        <span> - </span>
                        <span className={outletPriceClass}>{price.symbol}{price.outlet.toFixed(2)} ({discount.toFixed(0) + "% OFF"})</span>
                    </p>
                        <span>Quantity: {amount}</span>
                </Segment>
            </Segment.Group>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default OrderItem;