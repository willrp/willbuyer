//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState, useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import { Segment, Image, Label, Icon, Header, Select } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const segmentGroupClass = css({
    "&&&&&": {
        margin: "0",
        flexGrow: 1
    }
})

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
function CartItem({ id, name, image, price, discount, amount }) {
    const { updatingCart, updateCartItem, removeCartItem } = useContext(CartContext);
    const [quantity, setQuantity] = useState(amount);

    useEffect(() => {
        setQuantity(amount)
    }, [amount])

    function onChangeQuantity(e, { value }) {
        setQuantity(value);
        updateCartItem(id, value);
    }

    function onRemoveItem() {
        if(!updatingCart){
            removeCartItem(id);
        }
    }

    function render() {
        const maxquantity = (amount > 30) ? amount : 30;
        const options = [...Array(maxquantity).keys()].map(
            (item) => {
                return {
                    key: item + 1,
                    text: item + 1,
                    value: item + 1
                }
            }
        )

        return (
            <Segment.Group horizontal className={segmentGroupClass}>
                <Segment 
                    className={imgClass}
                    as={Link}
                    to={`/product/${id}`}
                >
                    <Image src={image.replace("wid=500", "wid=120")} alt=" " />
                </Segment>
                <Segment className={infoClass}>
                    <Label corner="right" onClick={onRemoveItem}>
                        <Icon name="x" fitted />
                    </Label>
                    <div className="headerdiv">
                        <Header size="small" as={Link} to={`/product/${id}`}>{name}</Header>
                    </div>
                    <p>
                        <span className={retailPriceClass}>{price.symbol}{price.retail.toFixed(2)}</span>
                        <span> - </span>
                        <span className={outletPriceClass}>{price.symbol}{price.outlet.toFixed(2)} ({discount.toFixed(0) + "% OFF"})</span>
                    </p>
                    <span>Quantity: </span>
                    <Select
                        compact
                        options={options}
                        value={quantity}
                        onChange={onChangeQuantity}
                        loading={updatingCart}
                        disabled={updatingCart}
                    />
                </Segment>
            </Segment.Group>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default CartItem;