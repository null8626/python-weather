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
  tocDrawer.style.visibility = 'visible'
}

// remove related pages in the footer
document.querySelector('.related-pages').remove()

// remove all header links
for (const headerLink of document.querySelectorAll('.headerlink')) {
  headerLink.remove()
}

for (const page of document.querySelectorAll('.sidebar-scroll li')) {
  const link = page.querySelector('a')
  const label = page.querySelector('label')

  if (label) {
    link.addEventListener('click', event => {
      event.preventDefault()
      label.click()
    })
  }
}