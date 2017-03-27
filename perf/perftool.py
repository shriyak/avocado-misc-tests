import os
import platform
from avocado import Test
from avocado import main
from avocado.utils import archive, build, distro, process
from avocado.utils.software_manager import SoftwareManager


class Perftool(Test):

    """
    perftool-testsuite
    """

    def setUp(self):
        '''
        Build perftool Test
        Source:
        https://github.com/rfmvh/perftool-testsuite
        '''

        # Check for basic utilities
        smm = SoftwareManager()
        detected_distro = distro.detect()
        kernel_ver = platform.uname()[2]
        deps = ['gcc', 'make']
        if 'Ubuntu' in detected_distro.name:
            deps.extend(['linux-tools-common', 'linux-tools-%s' % kernel_ver])
        elif detected_distro.name in ['redhat', 'SuSE', 'fedora']:
            deps.extend(['perf'])
        else:
            self.skip("Install the package for perf supported by %s"
                      % detected_distro.name)
        for package in deps:
            if not smm.check_installed(package) and not smm.install(package):
                self.skip('%s is needed for the test to be run' % package)

        locations = ["https://github.com/rfmvh/perftool-testsuite/archive/"
                     "master.zip"]
        tarball = self.fetch_asset("perftool.zip", locations=locations,
                                   expire='7d')
        archive.extract(tarball, self.srcdir)
        self.srcdir = os.path.join(self.srcdir, 'perftool-testsuite-master')

    def test(self):
        '''
        perf test :Does sanity tests
        Execute the tests by calling each module
        '''
        self.count = 0
        # Built in perf test
        for string in process.run("perf test").stderr.splitlines():
            if 'FAILED' in str(string.splitlines()):
                self.count += 1
                self.log.info("Test case failed is %s"
                              % str(string.splitlines()).strip("[]"))

        # perf testsuite
        for line in build.run_make(self.srcdir, extra_args='check',
                                   ignore_status=True).stdout.splitlines():
            if '-- [ FAIL ] --' in line:
                self.count += 1
                self.log.info(line)

        if self.count > 0:
            self.fail("%s Test failed" % self.count)


if __name__ == "__main__":
    main()
