//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Grid } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ResponsiveGrid from "components/util/responsive-grid";
import OrderItem from "./order-item";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const gridClass = css({
    "&&&&&": {
        margin: "0"
    }
})

const columnClass = css({
    "&&&&&": {
        padding: "0",
        display: "flex",
        justifyContent: "center"
    },
    "&&&&&>.segments": {
        margin: "0",
        flexGrow: 1
    }
})

//COMPONENT=================================================================
function OrderItems({ items }) {
    function renderItems() {
        let key = 0;
        return items.map(
            (item) => {
                key++;
                return (
                    <Grid.Column className={columnClass} key={key}>
                        <OrderItem {...item} />
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
export default OrderItems;