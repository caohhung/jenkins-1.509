#!/bin/bash

set -x
set -e
SPECFILE='specs/jenkins.spec'
PACKAGE='jenkins-1.509.4'

spectool -g $SPECFILE -s 5
rm -rfv $PACKAGE
tar -zxf $PACKAGE.tar.gz
mv jenkins-$PACKAGE $PACKAGE

pushd $PACKAGE
patch -p1 < ../0001-Apply-JENKINS-10234-to-jenkins-1.509.4.patch
export JAVA_HOME='/usr/lib/jvm/java-1.7.0'
export PATH=$JAVA_HOME/bin:$PATH
mvn -Plight-test install -Dlicense.disableCheck
cp war/target/jenkins.war ../jenkins.war
popd

rm -rf PACKAGE
mkdir -p PACKAGE.tar.gz

rpmbuild \
    --define "_sourcedir $PWD" \
    --define '_srcrpmdir srpm/' \
    --define 'dist .el7' \
    -bs "$SPECFILE"