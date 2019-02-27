developer=http://indiecomputing.com/
url=${developer}
maintainer=http://indiecomputing.com/
pkgname=$(basename $(pwd))
pkgver=0.15
pkgrel=1
pkgdesc="Host and work down task lists generated with taligen"
arch=('any')
license=("GPL")
options=('!strip')
depends=('python' 'ubos-rsync-server')

package() {
# Manifest
    install -D -m0644 ${startdir}/ubos-manifest.json ${pkgdir}/ubos/lib/ubos/manifests/${pkgname}.json

# Icons
#    install -D -m0644 ${startdir}/appicons/{72x72,144x144}.png -t ${pkgdir}/ubos/http/_appicons/${pkgname}/
#    install -D -m0644 ${startdir}/appicons/license.txt         -t ${pkgdir}/ubos/http/_appicons/${pkgname}/

# Generated config file goes here
    mkdir -p ${pkgdir}/ubos/lib/${pkgname}

# taliwodo user
    install -D -m0644 ${startdir}/sysusers.d/* -t ${pkgdir}/usr/lib/sysusers.d/

# CSS, Javascript
    install -D -m0644 ${startdir}/assets/* -t ${pkgdir}/ubos/share/${pkgname}/assets/

# Code
    install -D -m0755 ${startdir}/web/*.py -t ${pkgdir}/ubos/share/${pkgname}/web/
    for d in handlers model pages; do install -D -m0755 ${startdir}/web/$d/*.py -t ${pkgdir}/ubos/share/${pkgname}/web/$d/ ; done
    install -D -m0755 ${startdir}/tmpl/*.tmpl -t ${pkgdir}/ubos/share/${pkgname}/tmpl/
}
