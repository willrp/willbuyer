//IMPORT EXTERNAL COMPONENTS================================================
import React, { useContext } from "react";

//IMPORT INTERNAL COMPONENTS================================================
import ProductAddCart from "./product-add-cart";
import ProductViewCart from "./product-view-cart";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";

//COMPONENT=================================================================
function ProductCart({ productid }) {
    const { products } = useContext(CartContext);

    function isInCart(productid) {
        const index = products.findIndex((p) => {
            return p.id === productid
        })

        if(index === -1){
            return false;
        }
        else{
            return true;
        }
    }

    function render() {
        const incart = isInCart(productid);
        if(incart){
            return <ProductViewCart />
        }
        else{
            return <ProductAddCart productid={productid} />
        }
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default ProductCart;