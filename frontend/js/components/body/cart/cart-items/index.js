//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Grid } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ResponsiveGrid from "components/util/responsive-grid";
import CartItem from "./cart-item";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const gridClass = css({
    "&&&&&": {
        margin: "0",
        marginTop: "1em"
    }
})

const columnClass = css({
    "&&&&&": {
        padding: "0.25em",
        display: "flex"
    }
})

//COMPONENT=================================================================
function CartItems({ items }) {
    function renderItems() {
        let key = 0;
        return items.map(
            (item) => {
                key++;
                return (
                    <Grid.Column className={columnClass} key={key}>
                        <CartItem {...item} />
                    </Grid.Column>
                )
            }
        )
    }

    function render() {
        return (
            <ResponsiveGrid
                className={gridClass}
                largescreen={3}
                tablet={2}
                mobile={1}
            >
                {renderItems()}
            </ResponsiveGrid>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default CartItems;