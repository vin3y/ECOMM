var updateBtns= document.getElementsByClassName('update-cart');

for(var i=0;i<updateBtns.length;i++)
{
    updateBtns[i].addEventListener('click', function()
    {
        var productId=this.dataset.product
        var action = this.dataset.action
        console.log('productid:', productId,'action:' ,action )


        console.log('USER:', user);
        if(user === 'AnonymousUser')
        {
            console.log('login first');
        }
        else
        {
            updateUser(productId, action)
        }
    })

}

function updateUser(productId, action)
{
    console.log('User is logged in, pass the data');
    var url= '/update_item/'


    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action' : action
        })
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}