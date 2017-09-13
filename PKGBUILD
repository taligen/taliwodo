developer=http://indiecomputing.com/
url=${developer}
maintainer=http://indiecomputing.com/
pkgname=$(basename $(pwd))
pkgver=0.5
pkgrel=1
pkgdesc="Host and work down task lists generated with taligen"
arch=('any')
license=("GPL")
options=('!strip')
depends=('python' 'ubos-rsync-server')
install=install

package() {
# Manifest
    mkdir -p ${pkgdir}/var/lib/ubos/manifests
    install -m0644 ${startdir}/ubos-manifest.json ${pkgdir}/var/lib/ubos/manifests/${pkgname}.json

# Icons
#    mkdir -p ${pkgdir}/srv/http/_appicons/${pkgname}
#    install -m644 ${startdir}/appicons/{72x72,144x144}.png ${pkgdir}/srv/http/_appicons/${pkgname}/
#    install -m644 ${startdir}/appicons/license.txt ${pkgdir}/srv/http/_appicons/${pkgname}/

# Generated config file goes here
    mkdir -p ${pkgdir}/var/lib/${pkgname}

# CSS
    mkdir -p ${pkgdir}/usr/share/${pkgname}/css
    install -m644 ${startdir}/css/*.css ${pkgdir}/usr/share/${pkgname}/css/

# Code
    mkdir -p ${pkgdir}/usr/share/${pkgname}/web
    install -m755 ${startdir}/web/*.py ${pkgdir}/usr/share/${pkgname}/web/

    mkdir -p ${pkgdir}/usr/share/${pkgname}/tmpl
    install -m755 ${startdir}/tmpl/*.tmpl ${pkgdir}/usr/share/${pkgname}/tmpl/
}
