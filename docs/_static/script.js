const enumProperties = [...document.querySelectorAll('.property')].filter(x => x.parentElement.children.length === 3)

for (const enumProperty of enumProperties) {
  // we don't need to display enum values
  enumProperty.children[3].innerText = '...'
  
  // kill the rest of the children >:)
  for (let i = 4; i < enumProperty.children.length; i++) {
    enumProperty.children[i].remove()
  }
  
  // remove hyperlinks to enum properties as they are useless
  const parentChildren = enumProperty.parentElement.children
  
  parentChildren[parentChildren.length - 1].remove()
}

let control = false

document.addEventListener('keydown', event => {
  if (event.key === 'Control') {
    control = true;
  } else if (event.key === 'f' && control) {
    event.preventDefault()
    document.querySelector('.sidebar-search').select()
  }
})

document.addEventListener('keyup', event => {
  if (event.key === 'Control') {
    control = false;
  }
})