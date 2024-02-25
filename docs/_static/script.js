document.addEventListener('load', () => {
  try {
    document.querySelector('.edit-this-page').remove()
    
    // remove these useless crap that appears on official readthedocs builds
    document.querySelector('#furo-readthedocs-versions').remove()
    document.querySelector('.injected').remove()
  } catch {
    // we're building this locally, forget it
  }
})

const tocDrawer = document.querySelector('aside.toc-drawer')

if (document.querySelector('section#python-weather')) {
  // we don't need the right sidebar on the main landing page
  tocDrawer.remove()
} else {
  document.addEventListener('load', () => tocDrawer.style.visibility = 'visible')
  
  const enumProperties = [...document.querySelectorAll('.property')].filter(x => x.parentElement.children.length === 3)

  for (const enumProperty of enumProperties) {
    // we don't need to display enum values
    enumProperty.children[3].innerText = '...'
    
    // kill the rest of the children >:)
    for (let i = 4; i < enumProperty.children.length; i++) {
      enumProperty.children[i].remove()
    }
  }
}

// remove related pages in the footer
document.querySelector('.related-pages').remove()

// remove all header links
for (const headerLink of document.querySelectorAll('.headerlink')) {
  headerLink.remove()
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
    control = false
  }
})