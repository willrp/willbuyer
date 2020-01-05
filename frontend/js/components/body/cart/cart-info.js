//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Grid, Header, Statistic, Segment } from "semantic-ui-react";

//IMPORT HOOKS==============================================================
import useAnimatedCounter from "hooks/animated-counter";
import useIsPhone from "hooks/is-phone";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const gridClass = css({
    "&&&&&": {
        margin: "0",
        marginBottom: "1em"
    },
    "&&&&&>.column": {
        padding: "0"
    },
    "&&&&& .segment": {
        padding: "0.25em",
        width: "100%",
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
})

const priceClass = css({
    "&&&&& .titleClass": {
        fontWeight: "bold",
        marginBottom: "0.25em"
    },
    "&&&&& .priceMetaClass": {
        textDecoration: "line-through",
        opacity: 0.4,
        marginBottom: "0.5em"
    },
    "&&&&& .priceHeaderClass": {
        color: "red",
        marginTop: "0"
    }
})

const discountClass = css({
    "&&&&& .statistic>div": {
        color: "red"
    }
})

//COMPONENT=================================================================
function CartInfo({ productsType, itemCount, total }) {
    const productsvalue = useAnimatedCounter(productsType);
    const itemCountvalue = useAnimatedCounter(itemCount);

    const { symbol, retail, outlet } = total;
    const retailvalue = useAnimatedCounter(retail, false);
    const outletvalue = useAnimatedCounter(outlet, false);

    const discount = Math.floor((1.0 - (outlet / retail)) * 100);
    const discountvalue = useAnimatedCounter(discount);

    const isPhone = useIsPhone();

    function render() {
        return (
            <Grid
                className={gridClass}
                columns={4}
            >
                <Grid.Column>
                    <Segment textAlign="center">
                        <Statistic size={(isPhone) ? "small" : null}>
                            <Statistic.Value>{productsvalue}</Statistic.Value>
                            <Statistic.Label>{(productsvalue === 1) ? "Product" : "Products"}</Statistic.Label>
                        </Statistic>
                    </Segment>
                </Grid.Column>
                <Grid.Column>
                    <Segment textAlign="center">
                        <Statistic size={(isPhone) ? "small" : null}>
                            <Statistic.Value>{itemCountvalue}</Statistic.Value>
                            <Statistic.Label>{(itemCountvalue === 1) ? "Item" : "Items"}</Statistic.Label>
                        </Statistic>
                    </Segment>
                </Grid.Column>
                <Grid.Column>
                    <Segment textAlign="center" className={priceClass}>
                        <div>
                            <p className="titleClass">Total Price:</p>
                            <p className="priceMetaClass">{symbol}{retailvalue.toFixed(2)}</p>
                            <Header as="h2" className="priceHeaderClass">{symbol}{outletvalue.toFixed(2)}</Header>
                        </div>
                    </Segment>
                </Grid.Column>
                <Grid.Column>
                    <Segment textAlign="center" className={discountClass}>
                        <Statistic size={(isPhone) ? "small" : null}>
                            <Statistic.Value>{discountvalue}%</Statistic.Value>
                            <Statistic.Label>Off</Statistic.Label>
                        </Statistic>
                    </Segment>
                </Grid.Column>
            </Grid>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default CartInfo;