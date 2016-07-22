Name:           jenkins
Version:        1.509
Release:        4%{?dist}.gdc1
License:        MIT
Summary:        An extendable open source continuous integration server
Url:            https://jenkins-ci.org
Group:          Development/Tools/Building
Source:         %{name}-%{name}-%{version}.4.tar.gz
Source1:        %{name}.init
Source2:        %{name}.sysconfig
Source3:        %{name}.logrotate
Source4:        %{name}.repo
Source5:        %{name}.war
Patch1:         0001-Apply-JENKINS-10234-to-jenkins-1.509.4.patch
Requires:       java >= 1.7
Requires(pre):	maven
Requires(pre):	java >= 1.7
Provides:       hudson = %{version}
Obsoletes:      hudson < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Jenkins-CI monitors executions of repeated jobs, such as building a software
project or jobs run by cron. Among those things, current Jenkins-CI focuses
on the following two jobs:

   1. Building/testing software projects continuously, just like
      CruiseControl or DamageControl. In a nutshell, Jenkins-CI provides an
      easy-to-use so-called continuous integration system, making i
tjen      easier for developers to integrate changes to the project, and
      making it easier for users to obtain a fresh build. The automated,
      continuous build increases the productivity.
   2. Monitoring executions of externally-run jobs, such as cron jobs and
      procmail jobs, even those that are run on a remote machine. For
      example, with cron, all you receive is regular e-mails that capture
      the output, and it is up to you to look at them diligently and notice
      when it broke. Jenkins-CI keeps those outputs and makes it easy for you
      to notice when something is wrong.


%prep
%setup -q -c
rm -fv %{name}.war
pushd %{name}-%{name}-%{version}.4
%patch1 -p1
ls /usr/lib/jvm/java-1.7.0
mvn -Plight-test install -Dlicense.disableCheck
cp war/target/jenkins.war ../
popd

%build

%install
install -Dm0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/%{name}/%{name}.war
install -Dm0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
install -Dm0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -Dm0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -Dm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/yum.repos.d/%{name}.repo
install -d %{buildroot}%{_sbindir}
ln -sf ../../%{_sysconfdir}/init.d/%{name} %{buildroot}%{_sbindir}/rc%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}
install -d %{buildroot}%{_localstatedir}/cache/%{name}

%pre
groupadd -r jenkins &>/dev/null || :
useradd -g jenkins -s /bin/false -r -c "Jenkins Continuous Build server" -d /var/lib/jenkins jenkins &>/dev/null || :

%post

%preun
%stop_on_removal %{name}

%postun
%restart_on_update %{name}
%insserv_cleanup

%files
%defattr(-,root,root,,)
%{_sbindir}/rc%{name}
%{_prefix}/lib/%{name}
%config %{_sysconfdir}/init.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
#%%config(noreplace) %%{_sysconfdir}/sysconfig/%%{name}
%{_localstatedir}/adm/fillup-templates/sysconfig.%{name}
%attr(0755,jenkins,jenkins) %dir %{_localstatedir}/lib/%{name}
%attr(0755,jenkins,jenkins) %{_localstatedir}/log/%{name}

%changelog
